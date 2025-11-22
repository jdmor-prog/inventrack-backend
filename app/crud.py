from sqlmodel import select
from app import models, auth

def get_user_by_email(session, email: str):
    return session.exec(select(models.Usuario).where(models.Usuario.email == email)).first()

def get_user(session, user_id: int):
    return session.get(models.Usuario, user_id)

def create_user(session, user_data: dict):
    hashed = auth.get_password_hash(user_data["contraseña"])
    user = models.Usuario(
        nombre=user_data["nombre"],
        email=user_data["email"],
        contraseña=hashed,
        rol=user_data.get("rol", models.Role.Agricultor),
        ubicacion=user_data.get("ubicacion")
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def authenticate_user(session, email: str, password: str):
    user = get_user_by_email(session, email)
    if not user:
        return None
    if not auth.verify_password(password, user.contraseña):
        return None
    return user

# Cultivos
def create_cultivo(session, cultivo_data: dict):
    cultivo = models.Cultivo(**cultivo_data)
    session.add(cultivo)
    session.commit()
    session.refresh(cultivo)
    return cultivo

def get_cultivos_by_user(session, user_id: int):
    return session.exec(select(models.Cultivo).where(models.Cultivo.id_usuario == user_id)).all()

# Tareas
def create_tarea(session, tarea_data: dict):
    tarea = models.TareaAgricola(**tarea_data)
    session.add(tarea)
    session.commit()
    session.refresh(tarea)
    return tarea

def get_tareas_by_cultivo(session, cultivo_id: int):
    return session.exec(select(models.TareaAgricola).where(models.TareaAgricola.id_cultivo == cultivo_id)).all()
