from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session
from jose import jwt, JWTError
from app.database import get_session
from app.models import Usuario
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

SECRET_KEY = os.getenv("SECRET_KEY", "changeme123")
ALGORITHM = "HS256"

def get_db():
    yield from get_session()

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_db)) -> Usuario:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_str = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception
        user_id = int(user_id_str)
    except (JWTError, ValueError):
        raise credentials_exception

    user = session.get(Usuario, user_id)
    if not user:
        raise credentials_exception
    return user

def require_admin(current_user: Usuario = Depends(get_current_user)):
    # Asumimos que la relación 'rol' está cargada o se carga lazy.
    # Si es None, no tiene rol, por tanto no es admin.
    if not current_user.rol or current_user.rol.nombre_rol != "Administrador":
        raise HTTPException(status_code=403, detail="No tienes permisos de administrador")
    return current_user
