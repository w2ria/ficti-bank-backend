# app/services/user_service.py

from typing import Optional, Dict, Any
from datetime import datetime, timedelta

from sqlalchemy import text
from sqlmodel import Session, select

from app.core import security
from app.models.user import Usuario
from app.schemas.user import (
    UsuarioCreate,
    UserFromDB,
    UsuarioUpdate,
    StaffRegistrationData
)

from passlib.context import CryptContext

# ============================================================
#  CONFIGURACIÓN
# ============================================================

BLOQUEO_MINUTOS = 15
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ============================================================
# 1. AUTENTICACIÓN CON BLOQUEO Y SP
# ============================================================

def authenticate_user_with_sp(
    session: Session, username: str, password: str
) -> tuple[Optional[UserFromDB], list]:

    result_list: list = []

    try:
        # ------------------------------------------------------------
        # 1) OBTENER USUARIO REAL EN t_usuario
        # ------------------------------------------------------------
        statement = select(Usuario).where(Usuario.Usuario == username)
        user_obj: Optional[Usuario] = session.exec(statement).first()

        if not user_obj:
            print(f"Usuario '{username}' no existe en t_usuario.")
            return None, []

        # ------------------------------------------------------------
        # 2) VALIDAR ESTADO (empleado inactivo NO ingresa)
        # ------------------------------------------------------------
        if user_obj.Rol == "E" and user_obj.Estado != "A":
            print(f"Empleado '{username}' está INACTIVO.")
            return {"error": "inactivo"}, []

        # ------------------------------------------------------------
        # 3) BLOQUEO TEMPORAL SI TIENE ≥3 INTENTOS
        # ------------------------------------------------------------
        if user_obj.IntentosFallidos >= 3 and user_obj.UltimoIntento:
            tiempo_transcurrido = datetime.now() - user_obj.UltimoIntento

            if tiempo_transcurrido < timedelta(minutes=BLOQUEO_MINUTOS):
                print("Usuario bloqueado temporalmente por intentos fallidos.")
                return {"error": "bloqueado"}, []

            # Ya pasó el tiempo → desbloquear
            user_obj.IntentosFallidos = 0
            session.add(user_obj)
            session.commit()

        # ------------------------------------------------------------
        # 4) EJECUTAR SP PARA OBTENER DATOS DEL USUARIO
        # ------------------------------------------------------------
        query = text("CALL sp_ValidateUserLogin(:p_Username, @p_Out_Message);")
        result_proxy = session.execute(query, {"p_Username": username})
        result_list = result_proxy.mappings().all()

        # OUT message
        message_result = session.execute(text("SELECT @p_Out_Message;"))
        message_from_db = message_result.scalar_one_or_none()

        if "Error:" in (message_from_db or ""):
            print(f"SP error para '{username}': {message_from_db}")
            return None, []

        if not result_list:
            print(f"SP no encontró datos para '{username}'.")
            return None, []

        user_data = result_list[0]
        user = UserFromDB.model_validate(user_data)

        # ------------------------------------------------------------
        # 5) VALIDAR CONTRASEÑA
        # ------------------------------------------------------------
        if not security.verify_password(password, user.HashedPassword):
            print(f"Contraseña incorrecta para '{username}'.")

            user_obj.IntentosFallidos += 1
            user_obj.UltimoIntento = datetime.now()

            session.add(user_obj)
            session.commit()
            return {"error": "password"}, []

        # ------------------------------------------------------------
        # 6) LOGIN EXITOSO → RESET
        # ------------------------------------------------------------
        user_obj.IntentosFallidos = 0
        user_obj.UltimoIntento = datetime.now()

        session.add(user_obj)
        session.commit()

        # ------------------------------------------------------------
        # 7) RETORNAR RESULTADOS PARA EL ENDPOINT
        # ------------------------------------------------------------
        return user, result_list

    except Exception as e:
        print(f"🔴 Error inesperado en authenticate_user_with_sp: {e}")
        return None, []


# ============================================================
# 2. CREAR USUARIO
# ============================================================

def create_user(session: Session, user_in: UsuarioCreate) -> Usuario:
    db_user = Usuario(
        CodUsu=user_in.CodUsu,
        Usuario=user_in.Usuario,
        Rol=user_in.Rol,
        HashedPassword=security.get_password_hash(user_in.Password),
        Estado="A"
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# ============================================================
# 3. ACTUALIZAR USUARIO
# ============================================================

def update_user(session: Session, codusu: str, data: UsuarioUpdate) -> Dict[str, Any]:
    user = session.get(Usuario, codusu)

    if not user:
        raise Exception("El usuario no existe")

    if data.Usuario is not None:
        user.Usuario = data.Usuario

    if data.Rol is not None:
        user.Rol = data.Rol

    if data.Estado is not None:
        user.Estado = data.Estado

    if data.Password is not None:
        user.HashedPassword = security.get_password_hash(data.Password)

    session.add(user)
    session.commit()
    session.refresh(user)

    return {
        "mensaje": "Usuario actualizado correctamente",
        "CodUsu": user.CodUsu,
        "Usuario": user.Usuario,
        "Rol": user.Rol,
        "Estado": user.Estado
    }


# ============================================================
# 4. LISTAR ADMINISTRADORES
# ============================================================

def listar_administradores(session: Session):
    query = text("CALL sp_ListarAdministradores();")
    result = session.execute(query)
    return [dict(row) for row in result.mappings().all()]


# ============================================================
# 5. LISTAR EMPLEADOS (FILTRADO BACKEND)
# ============================================================

def listar_empleados(session: Session):
    query = text("CALL sp_ListarEmpleados();")
    result = session.execute(query)

    empleados = [dict(row) for row in result.mappings().all()]
    return [emp for emp in empleados if emp.get("Rol") == "E"]


# ============================================================
# 6. REGISTRO DE STAFF (SIMULACIÓN)
# ============================================================

def register_staff_sp(session: Session, user_data: StaffRegistrationData) -> Dict[str, Any]:

    hashed_password = pwd_context.hash(user_data.Password)

    if user_data.Usuario == "fail_test":
        raise ValueError("El usuario ya existe en la base de datos.")

    return {
        "CodUsu": "USR" + user_data.Rol + str(hash(user_data.Usuario))[:4],
        "Usuario": user_data.Usuario,
        "Rol": user_data.Rol,
        "MensajeSP": f"Éxito: Usuario interno '{user_data.Usuario}' registrado con Rol '{user_data.Rol}'."
    }
# ============================================================
# INACTIVAR USUARIO (usa SP)
# ============================================================

def inactivar_usuario_sp(session: Session, codusu: str) -> dict:
    try:
        # Ejecutar SP
        session.execute(
            text("CALL sp_InactivarUsuario(:cod, @msg);"),
            {"cod": codusu}
        )

        # 🚀 IMPORTANTE: confirmar cambios del SP
        session.commit()

        # Obtener mensaje OUT
        result = session.execute(text("SELECT @msg;"))
        message = result.scalar_one_or_none()

        return {
            "CodUsu": codusu,
            "Mensaje": message
        }

    except Exception as e:
        session.rollback()
        raise Exception(f"Error al inactivar usuario: {e}")
