from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from app.api.v1.deps import SessionDep
from app.core.security import create_access_token
from app.schemas.token import Token
from app.services import user_service

router = APIRouter()

@router.post("/token", response_model=Token)
def login_for_access_token(
    session: SessionDep, 
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    """
    Endpoint para el login de usuarios.
    Recibe 'username' y 'password' en un form-data.
    Devuelve el token y los datos del usuario en la variable 'result'.
    """

    print(f"Intentando autenticar al usuario: {form_data.username}")

    # Llamamos al servicio que maneja la lógica completa del login.
    user, result_data = user_service.authenticate_user_with_sp(
        session=session, 
        username=form_data.username, 
        password=form_data.password
    )

    # -----------------------------------------------------------
    # Manejo de errores especiales devueltos desde user_service
    # -----------------------------------------------------------

    # Caso: la función devolvió un diccionario de error
    if isinstance(user, dict):
        error = user.get("error")

        if error == "bloqueado":
            raise HTTPException(
                status_code=403,
                detail="Cuenta bloqueada temporalmente por múltiples intentos fallidos.",
            )

        if error == "inactivo":
            raise HTTPException(
                status_code=403,
                detail="El usuario está inactivo. Contacte al administrador.",
            )

        if error == "password":
            raise HTTPException(
                status_code=401,
                detail="Contraseña incorrecta.",
            )

    # Caso: autenticación fallida completamente (retorno None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nombre de usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # -----------------------------------------------------------
    # Login exitoso → crear token
    # -----------------------------------------------------------
    access_token = create_access_token(data={"sub": user.Usuario})

    # Convertimos los RowMappings en diccionarios JSON
    result_json_list = [dict(row) for row in result_data]

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "result": result_json_list
    }
