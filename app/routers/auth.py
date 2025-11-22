from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from app.database import get_session
from app.models import Usuario
from app.auth import verify_password, create_access_token
from app.schemas import Token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    # Buscar usuario por email (username en el form)
    statement = select(Usuario).where(Usuario.email == form_data.username)
    user = session.exec(statement).first()
    
    if not user or not verify_password(form_data.password, user.contraseña):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(subject=user.id_usuario)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/recover-password")
def recover_password(email: str, session: Session = Depends(get_session)):
    statement = select(Usuario).where(Usuario.email == email)
    user = session.exec(statement).first()
    
    if not user:
        # Por seguridad, no indicamos si el email existe o no, o mandamos mensaje genérico
        return {"message": "Si el correo existe, se ha enviado un token de recuperación."}
    
    # Simulación de envío de correo
    # En un caso real, aquí se generaría un token temporal y se enviaría por email
    return {"message": f"Se ha enviado un correo a {email} con las instrucciones (Simulado)."}

@router.post("/logout")
def logout():
    """
    Cierra la sesión del usuario.
    En una implementación con JWT sin estado (stateless), el servidor no necesita realizar ninguna acción
    más que confirmar la solicitud. El cliente (frontend) es responsable de eliminar el token almacenado.
    """
    return {"message": "Sesión cerrada exitosamente. Por favor elimine el token de acceso."}
