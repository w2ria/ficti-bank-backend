from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.api.v1.deps import SessionDep
from app.core.security import create_access_token
from app.schemas.token import Token
from app.services import user_service

router = APIRouter()

# 1ra versión
# @router.post("/token", response_model=Token)
# def login_for_access_token(
#     session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
# ):
#     # La lógica aquí usa las funciones actualizadas
#     user = user_service.authenticate_user(
#         session=session, username=form_data.username, password=form_data.password
#     )
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Usuario o contraseña incorrectos",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     # Guardamos el campo "Usuario" en el token
#     access_token = create_access_token(data={"sub": user.Usuario})
#     return {"access_token": access_token, "token_type": "bearer"}

@router.post("/token", response_model=Token)
def login_for_access_token(
    session: SessionDep, 
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    Endpoint para el login de usuarios.
    Recibe 'username' y 'password' en un form-data.
    """
    print(f"Intentando autenticar al usuario: {form_data.username}") # Un print para depurar

    user = user_service.authenticate_user_with_sp(
        session=session, username=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    # Si el login fue exitoso, `user` contiene los datos del usuario.
    # Usamos el nombre de usuario para crear el token JWT.
    access_token = create_access_token(data={"sub": user.Usuario}) # Usamos user.Usuario porque ahora es un objeto UserFromDB
    
    return {"access_token": access_token, "token_type": "bearer"}