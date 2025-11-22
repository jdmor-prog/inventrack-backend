import sys
import os

# Add the current directory to sys.path to make sure we can import app
sys.path.append(os.getcwd())

from sqlmodel import Session, select
from app.database import engine, init_db
from app.models import Rol, Usuario, Producto, Almacen, Stock, Entrada, Salida
from app.auth import get_password_hash
from datetime import datetime

def seed_data():
    print("Inicializando base de datos...")
    init_db()
    
    with Session(engine) as session:
        # Verificar si ya existen datos para no duplicar
        existing_roles = session.exec(select(Rol)).first()
        if existing_roles:
            print("La base de datos ya contiene datos. Saltando seed.")
            return

        print("Creando Roles...")
        rol_admin = Rol(nombre_rol="Administrador", descripcion="Acceso total al sistema")
        rol_almacenista = Rol(nombre_rol="Almacenista", descripcion="Gestión de inventario y movimientos")
        rol_vendedor = Rol(nombre_rol="Vendedor", descripcion="Consulta de stock y ventas")
        
        session.add(rol_admin)
        session.add(rol_almacenista)
        session.add(rol_vendedor)
        session.commit()
        
        session.refresh(rol_admin)
        session.refresh(rol_almacenista)
        session.refresh(rol_vendedor)

        print("Creando Usuarios...")
        # Contraseña para todos: "123456"
        hashed_pwd = get_password_hash("123456")
        
        user_admin = Usuario(
            email="admin@inventrack.com", 
            contraseña=hashed_pwd, 
            nombre="Admin User", 
            id_rol=rol_admin.id_rol
        )
        user_juan = Usuario(
            email="juan@inventrack.com", 
            contraseña=hashed_pwd, 
            nombre="Juan Perez", 
            id_rol=rol_almacenista.id_rol
        )
        user_maria = Usuario(
            email="maria@inventrack.com", 
            contraseña=hashed_pwd, 
            nombre="Maria Gomez", 
            id_rol=rol_vendedor.id_rol
        )
        
        session.add(user_admin)
        session.add(user_juan)
        session.add(user_maria)
        session.commit()
        
        session.refresh(user_admin)
        session.refresh(user_juan)
        session.refresh(user_maria)

        print("Creando Almacenes...")
        almacen_central = Almacen(nombre="Bodega Central")
        almacen_norte = Almacen(nombre="Sucursal Norte")
        almacen_sur = Almacen(nombre="Sucursal Sur")
        
        session.add(almacen_central)
        session.add(almacen_norte)
        session.add(almacen_sur)
        session.commit()
        
        session.refresh(almacen_central)
        session.refresh(almacen_norte)
        session.refresh(almacen_sur)

        print("Creando Productos...")
        prod_laptop = Producto(barcode="LP001", nombre="Laptop HP Pavilion", precio=1500.00)
        prod_mouse = Producto(barcode="MS001", nombre="Mouse Logitech Inalámbrico", precio=25.50)
        prod_teclado = Producto(barcode="KB001", nombre="Teclado Mecánico RGB", precio=80.00)
        prod_monitor = Producto(barcode="MN001", nombre="Monitor Dell 24 pulgadas", precio=200.00)
        
        session.add(prod_laptop)
        session.add(prod_mouse)
        session.add(prod_teclado)
        session.add(prod_monitor)
        session.commit()
        
        session.refresh(prod_laptop)
        session.refresh(prod_mouse)
        session.refresh(prod_teclado)
        session.refresh(prod_monitor)

        print("Inicializando Stock...")
        # Stock inicial en Bodega Central
        stock_laptop = Stock(id_producto=prod_laptop.id_producto, id_almacen=almacen_central.id_almacen, cantidad=50)
        stock_mouse = Stock(id_producto=prod_mouse.id_producto, id_almacen=almacen_central.id_almacen, cantidad=100)
        stock_teclado = Stock(id_producto=prod_teclado.id_producto, id_almacen=almacen_central.id_almacen, cantidad=75)
        stock_monitor = Stock(id_producto=prod_monitor.id_producto, id_almacen=almacen_central.id_almacen, cantidad=30)
        
        # Stock en Sucursal Norte
        stock_laptop_norte = Stock(id_producto=prod_laptop.id_producto, id_almacen=almacen_norte.id_almacen, cantidad=10)
        stock_mouse_norte = Stock(id_producto=prod_mouse.id_producto, id_almacen=almacen_norte.id_almacen, cantidad=20)

        session.add(stock_laptop)
        session.add(stock_mouse)
        session.add(stock_teclado)
        session.add(stock_monitor)
        session.add(stock_laptop_norte)
        session.add(stock_mouse_norte)
        session.commit()

        print("Registrando Entradas Iniciales (Histórico)...")
        entrada1 = Entrada(
            id_usuario=user_admin.id_usuario,
            id_almacen=almacen_central.id_almacen,
            id_producto=prod_laptop.id_producto,
            cantidad=50,
            observaciones="Inventario Inicial"
        )
        entrada2 = Entrada(
            id_usuario=user_juan.id_usuario,
            id_almacen=almacen_central.id_almacen,
            id_producto=prod_mouse.id_producto,
            cantidad=100,
            observaciones="Compra Lote #123"
        )
        
        session.add(entrada1)
        session.add(entrada2)
        session.commit()

        print("Base de datos poblada exitosamente!")

if __name__ == "__main__":
    seed_data()
