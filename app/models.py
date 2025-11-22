from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

# 1. Roles
class Rol(SQLModel, table=True):
    __tablename__ = "roles"
    
    id_rol: Optional[int] = Field(default=None, primary_key=True)
    nombre_rol: str
    descripcion: Optional[str] = None

    # Relaciones
    usuarios: List["Usuario"] = Relationship(back_populates="rol")


# 2. Usuarios
class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id_usuario: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    contraseña: str
    nombre: str
    fecha_registro: datetime = Field(default_factory=datetime.utcnow)
    id_rol: Optional[int] = Field(default=None, foreign_key="roles.id_rol")

    # Relaciones
    rol: Optional[Rol] = Relationship(back_populates="usuarios")
    entradas: List["Entrada"] = Relationship(back_populates="usuario")
    salidas: List["Salida"] = Relationship(back_populates="usuario")


# 3. Producto
class Producto(SQLModel, table=True):
    __tablename__ = "productos"

    id_producto: Optional[int] = Field(default=None, primary_key=True)
    barcode: str = Field(unique=True, index=True)
    nombre: str
    precio: float

    # Relaciones
    entradas: List["Entrada"] = Relationship(back_populates="producto")
    salidas: List["Salida"] = Relationship(back_populates="producto")
    stocks: List["Stock"] = Relationship(back_populates="producto")
    # Nota: La relación con Almacén es a través de Stock o directa si se requiere, 
    # pero el modelo dice "Almacén 1 — N Productos (en el contexto de asignación)" 
    # y "Producto 1 — N Almacenes" (vía Stock).
    # Se mantendrá la relación lógica vía Stock para inventario.
    almacenes_asignados: List["Almacen"] = Relationship(back_populates="producto_asignado")


# 4. Almacén
class Almacen(SQLModel, table=True):
    __tablename__ = "almacenes"

    id_almacen: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    # Atributo id_producto según requerimiento (Almacén asociado a un producto específico?)
    id_producto: Optional[int] = Field(default=None, foreign_key="productos.id_producto")

    # Relaciones
    producto_asignado: Optional[Producto] = Relationship(back_populates="almacenes_asignados")
    entradas: List["Entrada"] = Relationship(back_populates="almacen")
    stocks: List["Stock"] = Relationship(back_populates="almacen")


# 5. Entrada
class Entrada(SQLModel, table=True):
    __tablename__ = "entradas"

    id_entrada: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuarios.id_usuario")
    id_almacen: int = Field(foreign_key="almacenes.id_almacen")
    id_producto: int = Field(foreign_key="productos.id_producto")
    cantidad: int
    fecha_entrada: datetime = Field(default_factory=datetime.utcnow)
    observaciones: Optional[str] = None

    # Relaciones
    usuario: Optional[Usuario] = Relationship(back_populates="entradas")
    almacen: Optional[Almacen] = Relationship(back_populates="entradas")
    producto: Optional[Producto] = Relationship(back_populates="entradas")


# 6. Salida
class Salida(SQLModel, table=True):
    __tablename__ = "salidas"

    id_salida: Optional[int] = Field(default=None, primary_key=True)
    id_usuario: int = Field(foreign_key="usuarios.id_usuario")
    id_producto: int = Field(foreign_key="productos.id_producto")
    cantidad: int
    fecha_salida: datetime = Field(default_factory=datetime.utcnow)
    motivo: Optional[str] = None

    # Relaciones
    usuario: Optional[Usuario] = Relationship(back_populates="salidas")
    producto: Optional[Producto] = Relationship(back_populates="salidas")


# 7. Stock
class Stock(SQLModel, table=True):
    __tablename__ = "stock"

    id_stock: Optional[int] = Field(default=None, primary_key=True)
    id_producto: int = Field(foreign_key="productos.id_producto")
    id_almacen: int = Field(foreign_key="almacenes.id_almacen")
    cantidad: int = Field(default=0)

    # Relaciones
    producto: Optional[Producto] = Relationship(back_populates="stocks")
    almacen: Optional[Almacen] = Relationship(back_populates="stocks")
