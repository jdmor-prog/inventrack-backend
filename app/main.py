from fastapi import FastAPI
from app.database import init_db, get_session, engine
from app.routers import auth, users, products, warehouses, inventory
from app.models import Rol, Usuario
from app.auth import get_password_hash
from sqlmodel import Session, select

app = FastAPI(title="Inventrack API", version="1.0.0")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(warehouses.router)
app.include_router(inventory.router)

@app.on_event("startup")
def on_startup():
    init_db()
    create_initial_data()

def create_initial_data():
    with Session(engine) as session:
        # Crear Roles
        roles = ["Administrador", "Usuario"]
        for role_name in roles:
            role = session.exec(select(Rol).where(Rol.nombre_rol == role_name)).first()
            if not role:
                session.add(Rol(nombre_rol=role_name, descripcion=f"Rol de {role_name}"))
        session.commit()

        # Crear Admin por defecto
        admin_role = session.exec(select(Rol).where(Rol.nombre_rol == "Administrador")).first()
        if admin_role:
            admin_email = "admin@inventrack.com"
            admin = session.exec(select(Usuario).where(Usuario.email == admin_email)).first()
            if not admin:
                admin_user = Usuario(
                    email=admin_email,
                    contraseña=get_password_hash("admin123"),
                    nombre="Administrador Principal",
                    id_rol=admin_role.id_rol
                )
                session.add(admin_user)
                session.commit()
                print(f"Usuario Admin creado: {admin_email} / admin123")
