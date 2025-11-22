from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Almacen, Producto
from app.schemas import AlmacenCreate, AlmacenRead
from app.deps import get_current_user, require_admin

router = APIRouter(prefix="/warehouses", tags=["Almacenes"])

@router.post("/", response_model=AlmacenRead, dependencies=[Depends(require_admin)])
def create_warehouse(warehouse: AlmacenCreate, session: Session = Depends(get_session)):
    # Verificar si el producto asignado existe (si se proporciona)
    if warehouse.id_producto:
        prod = session.get(Producto, warehouse.id_producto)
        if not prod:
            raise HTTPException(status_code=404, detail="Producto asignado no encontrado")

    db_warehouse = Almacen.from_orm(warehouse)
    session.add(db_warehouse)
    session.commit()
    session.refresh(db_warehouse)
    return db_warehouse

@router.get("/", response_model=List[AlmacenRead])
def read_warehouses(current_user = Depends(get_current_user), session: Session = Depends(get_session)):
    # Admin y Usuario pueden ver
    warehouses = session.exec(select(Almacen)).all()
    return warehouses

@router.put("/{warehouse_id}", response_model=AlmacenRead, dependencies=[Depends(require_admin)])
def update_warehouse(warehouse_id: int, warehouse_update: AlmacenCreate, session: Session = Depends(get_session)):
    db_warehouse = session.get(Almacen, warehouse_id)
    if not db_warehouse:
        raise HTTPException(status_code=404, detail="Almacén no encontrado")
    
    if warehouse_update.id_producto:
        prod = session.get(Producto, warehouse_update.id_producto)
        if not prod:
            raise HTTPException(status_code=404, detail="Producto asignado no encontrado")
            
    db_warehouse.nombre = warehouse_update.nombre
    db_warehouse.id_producto = warehouse_update.id_producto
    
    session.add(db_warehouse)
    session.commit()
    session.refresh(db_warehouse)
    return db_warehouse
