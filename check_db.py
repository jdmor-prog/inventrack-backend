from sqlmodel import Session, select
from app.database import engine
from app.models import Usuario

def check_user():
    with Session(engine) as session:
        user = session.exec(select(Usuario).where(Usuario.email == "admin@inventrack.com")).first()
        if user:
            print(f"User found: {user.email}, ID: {user.id_usuario}, Hash: {user.contraseña[:10]}...")
        else:
            print("User NOT found in current DB configuration.")

if __name__ == "__main__":
    check_user()
