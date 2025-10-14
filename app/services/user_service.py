# app/services/user_service.py

# --- 1. Importaciones Corregidas y Completas ---
from typing import Optional, Dict, Any
from sqlmodel import Session, select
from sqlalchemy import text
from app.core import security
from app.models.user import Usuario
from app.schemas.user import UsuarioCreate, UserFromDB


# --- 2. Función de Autenticación con Stored Procedure (Mejorada) ---

def authenticate_user_with_sp(session: Session, username: str, password: str) -> Optional[UserFromDB]:
    """
    Autentica a un usuario llamando al SP sp_ValidateUserLogin de forma robusta.
    """
    try:
        # 1. Preparamos y ejecutamos la llamada al SP.
        #    Nota: Ya no necesitamos declarar el OUT param para SQLAlchemy aquí.
        query = text("CALL sp_ValidateUserLogin(:p_Username, @p_Out_Message);")
        result_proxy = session.execute(query, {"p_Username": username})
        
        # 2. Leemos el resultado del SELECT que devuelve el SP.
        user_data_from_db = result_proxy.mappings().first()

        # 3. ¡EL CAMBIO CLAVE! Ejecutamos una segunda consulta para obtener el valor del parámetro OUT.
        #    Esta es la forma más explícita y confiable.
        message_result = session.execute(text("SELECT @p_Out_Message;"))
        message_from_db = message_result.scalar_one_or_none()

        # --- LÓGICA DE VALIDACIÓN EN PYTHON ---

        if "Error:" in (message_from_db or ""):
            print(f"Error desde la BD para usuario '{username}': {message_from_db}")
            return None

        if not user_data_from_db:
            return None

        user = UserFromDB.model_validate(user_data_from_db)

        if not security.verify_password(password, user.HashedPassword):
            return None

        return user

    except Exception as e:
        print(f"🔴 Ocurrió una excepción inesperada durante la autenticación: {e}")
        # Opcional: para una depuración más profunda, puedes añadir esto:
        # import traceback
        # traceback.print_exc()
        return None


# --- 3. Función para Crear Usuario (ya la tenías) ---

def create_user(session: Session, user_in: UsuarioCreate) -> Usuario:
    """
    Crea un nuevo usuario en la base de datos.
    """
    db_user = Usuario(
        CodUsu=user_in.CodUsu,
        Usuario=user_in.Usuario,
        Rol=user_in.Rol,
        HashedPassword=security.get_password_hash(user_in.Password),
        Estado='A'  # 'A' de Activo por defecto
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user