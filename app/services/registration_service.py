# app/services/registration_service.py
from sqlmodel import Session
from sqlalchemy import text  # ¡Importante! Para ejecutar SQL de forma segura

from app.schemas.registration import FullClientRegistration
from app.core.security import get_password_hash


def register_client_with_sp(session: Session, reg_data: FullClientRegistration) -> dict:
    """
    Crea un nuevo Usuario y Cliente llamando al procedimiento almacenado sp_RegisterFullClientAndUser.
    """
    user_data = reg_data.user_data
    client_data = reg_data.client_data

    # 1. La encriptación de la contraseña SIEMPRE se hace en Python, nunca en la BD.
    hashed_password = get_password_hash(user_data.Password)

    # 2. Preparamos la llamada al procedimiento almacenado.
    # Usamos `text()` para prevenir inyección SQL. Los parámetros se nombran con `:nombre`.
    # Los parámetros OUT se declaran con `@_nombre` para que SQLAlchemy sepa que debe recuperarlos.
    query = text("""
        CALL sp_RegisterFullClientAndUser(
            :p_Usuario, :p_Password, :p_Rol,
            :p_Nombres, :p_Apellidos, :p_DNI, :p_Email, :p_FechaNac,
            :p_Direccion, :p_CodUbigeo, :p_Telefonos, :p_Movil,
            @_p_Out_CodUsu, @_p_Out_CodCliente, @_p_Out_Message
        );
    """)

    # 3. Ejecutamos la consulta pasando los valores en un diccionario.
    # Las claves del diccionario DEBEN coincidir con los nombres de los parámetros en `text()`.
    result = session.execute(query, {
        "p_Usuario": user_data.Usuario,
        "p_Password": hashed_password,
        "p_Rol": user_data.Rol,
        "p_Nombres": client_data.Nombres,
        "p_Apellidos": client_data.Apellidos,
        "p_DNI": client_data.DNI,
        "p_Email": client_data.e_mail,
        "p_FechaNac": client_data.Fecha_Nac,
        "p_Direccion": client_data.Direccion,
        "p_CodUbigeo": client_data.CodUbigeo,
        "p_Telefonos": client_data.Telefonos,
        "p_Movil": client_data.Movil
    })
    
    # 4. Es CRUCIAL hacer commit para que los parámetros OUT se actualicen.
    session.commit()
    
    # 5. Recuperamos los valores de los parámetros de SALIDA (OUT)
    # SQLAlchemy los guarda en el atributo `out_params` del resultado.
    out_params = result.out_params
    error_message = out_params.get('_p_Out_Message')  # El `_` es por la sintaxis `@_`

    # Si el SP devolvió un mensaje de error, lanzamos una excepción en Python
    if error_message != "OK":
        raise ValueError(error_message)

    # 6. Si todo salió bien, devolvemos los códigos generados
    return {
        "CodUsu": out_params.get('_p_Out_CodUsu'),
        "CodCliente": out_params.get('_p_Out_CodCliente')
    }
