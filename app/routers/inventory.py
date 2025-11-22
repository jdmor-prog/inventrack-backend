from typing import List
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, select
from app.database import get_session
from app.models import Entrada, Salida, Stock, Producto, Almacen
from app.schemas import EntradaCreate, EntradaRead, SalidaCreate, SalidaRead, StockRead
from app.deps import get_current_user, require_admin
import csv
import io

router = APIRouter(prefix="/inventory", tags=["Inventario"])

@router.post("/entry", response_model=EntradaRead)
def create_entry(entry: EntradaCreate, current_user = Depends(get_current_user), session: Session = Depends(get_session)):
    # Verificar producto y almacén
    product = session.get(Producto, entry.id_producto)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    warehouse = session.get(Almacen, entry.id_almacen)
    if not warehouse:
        raise HTTPException(status_code=404, detail="Almacén no encontrado")

    # Crear registro de entrada
    db_entry = Entrada(
        id_usuario=current_user.id_usuario,
        id_almacen=entry.id_almacen,
        id_producto=entry.id_producto,
        cantidad=entry.cantidad,
        observaciones=entry.observaciones
    )
    session.add(db_entry)

    # Actualizar Stock
    stock = session.exec(select(Stock).where(Stock.id_producto == entry.id_producto, Stock.id_almacen == entry.id_almacen)).first()
    if not stock:
        stock = Stock(id_producto=entry.id_producto, id_almacen=entry.id_almacen, cantidad=0)
        session.add(stock)
    
    stock.cantidad += entry.cantidad
    
    session.commit()
    session.refresh(db_entry)
    return db_entry

@router.post("/exit", response_model=SalidaRead)
def create_exit(exit_data: SalidaCreate, current_user = Depends(get_current_user), session: Session = Depends(get_session)):
    # Verificar producto
    product = session.get(Producto, exit_data.id_producto)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Verificar stock total (sumando todos los almacenes o especificando almacén? 
    # El modelo de Salida NO tiene id_almacen, solo id_producto. 
    # Esto es un problema si el producto está en múltiples almacenes.
    # Asumiremos FIFO o descuento de un almacén por defecto o error?
    # El modelo de Salida dice: id_salida, id_usuario, cantidad, fecha_salida, id_producto, motivo.
    # NO HAY ALMACEN EN SALIDA.
    # Esto implica que la salida descuenta del stock global o hay que elegir un almacén arbitrario.
    # Vamos a buscar stock disponible en cualquier almacén y descontar.
    
    stocks = session.exec(select(Stock).where(Stock.id_producto == exit_data.id_producto, Stock.cantidad > 0)).all()
    total_stock = sum(s.cantidad for s in stocks)
    
    if total_stock < exit_data.cantidad:
        raise HTTPException(status_code=400, detail="Stock insuficiente")

    remaining_to_deduct = exit_data.cantidad
    
    # Descontar de los almacenes disponibles (estrategia simple)
    for stock in stocks:
        if remaining_to_deduct <= 0:
            break
        if stock.cantidad >= remaining_to_deduct:
            stock.cantidad -= remaining_to_deduct
            remaining_to_deduct = 0
        else:
            remaining_to_deduct -= stock.cantidad
            stock.cantidad = 0
        session.add(stock)

    # Crear registro de salida
    db_exit = Salida(
        id_usuario=current_user.id_usuario,
        id_producto=exit_data.id_producto,
        cantidad=exit_data.cantidad,
        motivo=exit_data.motivo
    )
    session.add(db_exit)
    session.commit()
    session.refresh(db_exit)
    return db_exit

@router.get("/stock", response_model=List[StockRead])
def read_stock(current_user = Depends(get_current_user), session: Session = Depends(get_session)):
    # Admin y Usuario pueden ver stock actual
    stocks = session.exec(select(Stock)).all()
    return stocks

@router.get("/movements/entries", response_model=List[EntradaRead], dependencies=[Depends(require_admin)])
def read_entries(session: Session = Depends(get_session)):
    return session.exec(select(Entrada)).all()

@router.get("/movements/exits", response_model=List[SalidaRead], dependencies=[Depends(require_admin)])
def read_exits(session: Session = Depends(get_session)):
    return session.exec(select(Salida)).all()

@router.get("/alerts", dependencies=[Depends(require_admin)])
def read_alerts(session: Session = Depends(get_session)):
    # Alerta de stock bajo (< 10 unidades por ejemplo)
    low_stock = session.exec(select(Stock).where(Stock.cantidad < 10)).all()
    return low_stock

@router.get("/export/csv", dependencies=[Depends(require_admin)])
def export_inventory(session: Session = Depends(get_session)):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID Stock', 'Producto', 'Almacen', 'Cantidad'])
    
    stocks = session.exec(select(Stock)).all()
    for stock in stocks:
        p_name = stock.producto.nombre if stock.producto else "Unknown"
        a_name = stock.almacen.nombre if stock.almacen else "Unknown"
        writer.writerow([stock.id_stock, p_name, a_name, stock.cantidad])
        
    output.seek(0)
    return Response(content=output.getvalue(), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=inventory.csv"})
