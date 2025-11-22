from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models import Usuario, Rol
from app.schemas import UsuarioCreate, UsuarioRead, UsuarioUpdate
from app.deps import get_current_user, require_admin
from app.auth import get_password_hash

router = APIRouter(prefix="/users", tags=["Usuarios"])

@router.post("/", response_model=UsuarioRead, dependencies=[Depends(require_admin)])
def create_user(user: UsuarioCreate, session: Session = Depends(get_session)):
    # Verificar si el email ya existe
    existing_user = session.exec(select(Usuario).where(Usuario.email == user.email)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    # Asignar rol por defecto si no se envía, o verificar si el rol existe
    if user.id_rol:
        rol = session.get(Rol, user.id_rol)
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
    
    hashed_password = get_password_hash(user.contraseña)
    db_user = Usuario.from_orm(user)
    db_user.contraseña = hashed_password
    
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.get("/", response_model=List[UsuarioRead], dependencies=[Depends(require_admin)])
def read_users(session: Session = Depends(get_session)):
    users = session.exec(select(Usuario)).all()
    return users

@router.put("/me", response_model=UsuarioRead)
def update_me(user_update: UsuarioUpdate, current_user: Usuario = Depends(get_current_user), session: Session = Depends(get_session)):
    # Usuario actualizando sus propios datos
    if user_update.nombre:
        current_user.nombre = user_update.nombre
    if user_update.email:
        # Verificar unicidad si cambia email
        if user_update.email != current_user.email:
            existing = session.exec(select(Usuario).where(Usuario.email == user_update.email)).first()
            if existing:
                raise HTTPException(status_code=400, detail="El email ya está en uso")
            current_user.email = user_update.email
    if user_update.contraseña:
        current_user.contraseña = get_password_hash(user_update.contraseña)
    
    # Usuarios normales no pueden cambiar su rol
    
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user

@router.put("/{user_id}", response_model=UsuarioRead, dependencies=[Depends(require_admin)])
def update_user(user_id: int, user_update: UsuarioUpdate, session: Session = Depends(get_session)):
    db_user = session.get(Usuario, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    if user_update.nombre:
        db_user.nombre = user_update.nombre
    if user_update.email:
        if user_update.email != db_user.email:
            existing = session.exec(select(Usuario).where(Usuario.email == user_update.email)).first()
            if existing:
                raise HTTPException(status_code=400, detail="El email ya está en uso")
            db_user.email = user_update.email
    if user_update.contraseña:
        db_user.contraseña = get_password_hash(user_update.contraseña)
    if user_update.id_rol:
        rol = session.get(Rol, user_update.id_rol)
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        db_user.id_rol = user_update.id_rol
        
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
