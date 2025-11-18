# app/api/v1/endpoints/embargos.py

from fastapi import APIRouter, HTTPException, status
import traceback
from typing import Dict, Any, List

# --- Dependencias ---
from app.api.v1.deps import SessionDep
from app.schemas.util import APIResponse
from app.schemas.embargos import EmbargoCreate
from app.services import embargos_service

router = APIRouter()


# ============================================================
# 1. REGISTRAR EMBARGO (TOTAL O PARCIAL)
# ============================================================
@router.post(
    "/registrarEmbargo",
    response_model=APIResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registra un nuevo embargo (total o parcial) en una cuenta."
)
def registrar_embargo(
    *,
    session: SessionDep,
    datos_embargo: EmbargoCreate,
):
    """
    Registra un embargo utilizando el SP sp_RegistrarEmbargo.
    """
    try:
        resultado_sp: Dict[str, Any] = embargos_service.registrar_embargo_sp(
            session=session,
            datos_embargo=datos_embargo,
        )

        return APIResponse(
            mensaje=resultado_sp["MensajeSP"],
            codigo=str(resultado_sp["IdEmbargo"]),
            status_code=status.HTTP_201_CREATED,
            result=[resultado_sp]
        )

    except ValueError as ve:
        error_message = str(ve)
        error_code = (
            status.HTTP_404_NOT_FOUND
            if "no existe" in error_message.lower()
            else status.HTTP_400_BAD_REQUEST
        )

        raise HTTPException(
            status_code=error_code,
            detail=APIResponse(
                mensaje=error_message,
                codigo="EMBARGO-ERR",
                status_code=error_code
            ).model_dump()
        )

    except Exception as e:
        print("🔴 ERROR INESPERADO AL REGISTRAR EMBARGO:", e)
        traceback.print_exc()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=APIResponse(
                mensaje="Error interno del servidor.",
                codigo="SYS-500",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).model_dump()
        )


# ============================================================
# 2. LISTAR EMBARGOS POR CUENTA
# ============================================================
@router.get(
    "/listarEmbargos/{nrocta}",
    response_model=APIResponse,
    status_code=status.HTTP_200_OK,
    summary="Lista todos los embargos asociados a una cuenta."
)
def listar_embargos_por_cuenta(
    nrocta: str,
    session: SessionDep
):
    """
    Lista los embargos asociados a un número de cuenta usando el SP sp_ListarEmbargosPorCuenta.
    """
    try:
        lista = embargos_service.listar_embargos_por_cuenta_sp(
            session=session,
            nrocta=nrocta
        )

        return APIResponse(
            mensaje="Embargos listados correctamente.",
            codigo="OK",
            status_code=status.HTTP_200_OK,
            result=lista
        )

    except ValueError as ve:
        error_message = str(ve)
        error_code = (
            status.HTTP_404_NOT_FOUND
            if "no existe" in error_message.lower()
            else status.HTTP_400_BAD_REQUEST
        )

        raise HTTPException(
            status_code=error_code,
            detail=APIResponse(
                mensaje=error_message,
                codigo="EMBARGO-ERR",
                status_code=error_code
            ).model_dump()
        )

    except Exception as e:
        print("🔴 ERROR INESPERADO AL LISTAR EMBARGOS:", e)
        traceback.print_exc()

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=APIResponse(
                mensaje="Error interno del servidor.",
                codigo="SYS-500",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            ).model_dump()
        )
