from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Producto
from app.schemas import ProductoCreate, ProductoRead, ProductoUpdate
from app.deps import get_current_user, require_admin

router = APIRouter(prefix="/products", tags=["Productos"])

@router.post("/", response_model=ProductoRead)
def create_product(product: ProductoCreate, current_user = Depends(get_current_user), session: Session = Depends(get_session)):
    # Admin y Usuario pueden crear
    existing = session.exec(select(Producto).where(Producto.barcode == product.barcode)).first()
    if existing:
        raise HTTPException(status_code=400, detail="El código de barras ya existe")
    
    db_product = Producto.from_orm(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@router.get("/", response_model=List[ProductoRead])
def read_products(session: Session = Depends(get_session)):
    # Acceso anónimo permitido
    products = session.exec(select(Producto)).all()
    return products

@router.get("/barcode/{barcode}", response_model=ProductoRead)
def analyze_barcode(barcode: str, session: Session = Depends(get_session)):
    # Acceso anónimo permitido
    product = session.exec(select(Producto).where(Producto.barcode == barcode)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.put("/{product_id}", response_model=ProductoRead)
def update_product(product_id: int, product_update: ProductoUpdate, current_user = Depends(get_current_user), session: Session = Depends(get_session)):
    # Admin y Usuario pueden editar
    db_product = session.get(Producto, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    if product_update.barcode:
        if product_update.barcode != db_product.barcode:
            existing = session.exec(select(Producto).where(Producto.barcode == product_update.barcode)).first()
            if existing:
                raise HTTPException(status_code=400, detail="El código de barras ya existe")
            db_product.barcode = product_update.barcode
            
    if product_update.nombre:
        db_product.nombre = product_update.nombre
    if product_update.precio is not None:
        db_product.precio = product_update.precio
        
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@router.delete("/{product_id}", dependencies=[Depends(require_admin)])
def delete_product(product_id: int, session: Session = Depends(get_session)):
    # Solo Admin puede eliminar
    db_product = session.get(Producto, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    session.delete(db_product)
    session.commit()
    return {"ok": True}
