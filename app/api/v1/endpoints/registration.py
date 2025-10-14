# app/api/v1/endpoints/registration.py
from fastapi import APIRouter, HTTPException
import traceback # Útil para depurar errores inesperados

# Importamos las dependencias que preparan la sesión de BD
from app.api.v1.deps import SessionDep

# Importamos el schema que valida los datos de entrada
from app.schemas.registration import FullClientRegistration

# ¡LA IMPORTACIÓN CLAVE! Importamos nuestro módulo de servicios
from app.services import registration_service

router = APIRouter()

@router.post("/", status_code=201) 
def register_full_client(
    *,
    session: SessionDep,
    registration_data: FullClientRegistration
):
    """
    Endpoint público para registrar un nuevo cliente y su usuario de acceso
    utilizando un procedimiento almacenado.
    """
    try:
        # ==================================================================
        # ¡AQUÍ ES DONDE EL ENDPOINT LLAMA A LA FUNCIÓN DEL SERVICIO!
        # ==================================================================
        # Le pasamos la sesión de la base de datos y los datos de registro
        # que ya fueron validados por FastAPI.
        new_ids = registration_service.register_client_with_sp(
            session=session, reg_data=registration_data
        )
        # ==================================================================
        
        # Si el servicio termina sin errores, devolvemos una respuesta de éxito.
        return {"message": "Cliente y usuario registrados con éxito", "generated_ids": new_ids}
    
    except ValueError as ve:
        # Capturamos los errores de negocio que devuelve el SP (ej: DNI duplicado)
        # 409 Conflict es el código ideal para este tipo de error.
        raise HTTPException(status_code=409, detail=str(ve))
    
    except Exception as e:
        # Capturamos cualquier otro error inesperado que no sea un ValueError
        print("🔴 OCURRIÓ UN ERROR INESPERADO EN EL ENDPOINT DE REGISTRO:")
        traceback.print_exc() # Imprime el error detallado en la consola del servidor
        
        raise HTTPException(status_code=500, detail=f"Ocurrió un error interno en el servidor.")