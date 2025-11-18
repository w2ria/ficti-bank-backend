from typing import Dict, Any, List
from sqlmodel import Session
from sqlalchemy import text
from app.schemas.embargos import EmbargoCreate


# ============================================================
# 1. REGISTRAR EMBARGO - SP REAL (6 PARÁMETROS)
# ============================================================
def registrar_embargo_sp(session: Session, datos_embargo: EmbargoCreate) -> Dict[str, Any]:

    try:
        query = text("""
            CALL sp_RegistrarEmbargo(
                :p_NroCta,
                :p_TipoEmbargo,
                :p_MontoEmbargado,
                :p_UsrRegistro,
                @p_Out_IdEmbargo,
                @p_Out_Message
            );
        """)

        params = {
            "p_NroCta": datos_embargo.NroCta,
            "p_TipoEmbargo": datos_embargo.TipoEmbargo,
            "p_MontoEmbargado": datos_embargo.MontoEmbargado,
            "p_UsrRegistro": datos_embargo.CodUsu
        }

        # Ejecutar SP
        session.execute(query, params)

        # 🔥🔥 COMMIT obligatorio
        session.commit()

        # Leer OUT parameters
        result = session.execute(text("""
            SELECT 
                @p_Out_IdEmbargo AS IdEmbargo,
                @p_Out_Message AS MensajeSP;
        """)).mappings().first()

        result = dict(result)

        # Validar errores del SP
        if result["MensajeSP"].startswith("Error:"):
            raise ValueError(result["MensajeSP"])

        return result

    except ValueError:
        raise

    except Exception as e:
        print("🔴 Error interno en registrar_embargo_sp:", e)
        raise Exception(f"Error interno al registrar embargo: {e}")


# ============================================================
# 2. LISTAR EMBARGOS POR CUENTA
# ============================================================
def listar_embargos_por_cuenta_sp(session: Session, nrocta: str) -> List[Dict[str, Any]]:
    try:
        res = session.execute(
            text("CALL sp_ListarEmbargosPorCuenta(:nrocta);"),
            {"nrocta": nrocta}
        )
        
        # 🔥 IMPORTANTE: algunos SP requieren commit
        session.commit()

        return [dict(r) for r in res.mappings().all()]

    except Exception as e:
        print("🔴 Error en listar_embargos_por_cuenta_sp:", e)
        raise ValueError(f"Error al listar embargos: {e}")
