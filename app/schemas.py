from datetime import datetime
from sqlmodel import SQLModel
from typing import Optional, List

# Token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(SQLModel):
    email: Optional[str] = None

# Roles
class RolCreate(SQLModel):
    nombre_rol: str
    descripcion: Optional[str] = None

class RolRead(RolCreate):
    id_rol: int

# Usuarios
class UsuarioBase(SQLModel):
    email: str
    nombre: str
    id_rol: Optional[int] = None

class UsuarioCreate(UsuarioBase):
    contraseña: str

class UsuarioRead(UsuarioBase):
    id_usuario: int
    fecha_registro: datetime
    rol: Optional[RolRead] = None

class UsuarioUpdate(SQLModel):
    email: Optional[str] = None
    nombre: Optional[str] = None
    contraseña: Optional[str] = None
    id_rol: Optional[int] = None

# Productos
class ProductoBase(SQLModel):
    barcode: str
    nombre: str
    precio: float

class ProductoCreate(ProductoBase):
    pass

class ProductoRead(ProductoBase):
    id_producto: int

class ProductoUpdate(SQLModel):
    barcode: Optional[str] = None
    nombre: Optional[str] = None
    precio: Optional[float] = None

# Almacenes
class AlmacenBase(SQLModel):
    nombre: str
    id_producto: Optional[int] = None

class AlmacenCreate(AlmacenBase):
    pass

class AlmacenRead(AlmacenBase):
    id_almacen: int
    producto_asignado: Optional[ProductoRead] = None

# Entradas
class EntradaCreate(SQLModel):
    id_almacen: int
    id_producto: int
    cantidad: int
    observaciones: Optional[str] = None

class EntradaRead(SQLModel):
    id_entrada: int
    id_usuario: int
    id_almacen: int
    id_producto: int
    cantidad: int
    fecha_entrada: datetime
    observaciones: Optional[str] = None
    producto: Optional[ProductoRead] = None
    almacen: Optional[AlmacenRead] = None
    usuario: Optional[UsuarioRead] = None

# Salidas
class SalidaCreate(SQLModel):
    id_producto: int
    cantidad: int
    motivo: Optional[str] = None

class SalidaRead(SQLModel):
    id_salida: int
    id_usuario: int
    id_producto: int
    cantidad: int
    fecha_salida: datetime
    motivo: Optional[str] = None
    producto: Optional[ProductoRead] = None
    usuario: Optional[UsuarioRead] = None

# Stock
class StockRead(SQLModel):
    id_stock: int
    id_producto: int
    id_almacen: int
    cantidad: int
    producto: Optional[ProductoRead] = None
    almacen: Optional[AlmacenRead] = None
