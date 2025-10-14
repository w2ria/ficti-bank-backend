# app/api/v1/endpoints/registration.py
from fastapi import APIRouter, HTTPException
from app.api.v1.deps import SessionDep
from app.schemas.registration import FullClientRegistration  # Mantenemos el schema de entrada
from app.services import registration_service
import traceback

router = APIRouter()


# Cambiamos el response_model porque ya no devolvemos el objeto completo.
# El status_code 201 (Created) sigue siendo el correcto.
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
        # Llamamos a nuestra nueva función de servicio que usa el SP
        new_ids = registration_service.register_client_with_sp(
            session=session, reg_data=registration_data
        )
        # Devolvemos una respuesta clara con los nuevos IDs
        return {"message": "Cliente y usuario registrados con éxito", "generated_ids": new_ids}
    
    except ValueError as ve:
        # Capturamos los errores de negocio que devuelve el SP (ej: DNI duplicado)
        # 409 Conflict es el código ideal para este tipo de error.
        raise HTTPException(status_code=409, detail=str(ve))
    
    except Exception as e:
        # print("🔴 OCURRIÓ UN ERROR INESPERADO:")
        # traceback.print_exc()
        
        # Capturamos cualquier otro error inesperado
        raise HTTPException(status_code=500, detail=f"Ocurrió un error interno: {e}")
