from fastapi import APIRouter
from app.api.v1.deps import SessionDep, CurrentUser
from app.services import user_service
from typing import Optional
from sqlmodel import Field, SQLModel
from app.schemas.user import UsuarioCreate, UsuarioPublic # Cambiar a los nuevos schemas

router = APIRouter()

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True)
    hashed_password: str
    full_name: Optional[str] = None
    role: str = Field(default="Empleado") # Empleado o Administrador
    is_active: bool = Field(default=True)
    

@router.post("/", response_model=UsuarioPublic)
def register_user(session: SessionDep, user_in: UsuarioCreate):
    # Llama al servicio de creación de usuario actualizado
    return user_service.create_user(session=session, user_in=user_in)

@router.get("/me", response_model=UsuarioPublic)
def read_users_me(current_user: CurrentUser):
    # Esto funciona directamente gracias a la dependencia `CurrentUser` actualizada
    return current_user