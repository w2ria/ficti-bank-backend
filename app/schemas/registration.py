from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import date

# ===============================================================
# SCHEMAS PARA LA ENTRADA DE DATOS (REQUEST BODY)
# ===============================================================

class UserRegistrationData(SQLModel):
    """
    Define los datos necesarios para crear un nuevo usuario
    durante el registro del cliente.
    """
    Usuario: str = Field(..., description="Nombre de usuario para el login, ej: 'jperez'")
    Password: str = Field(..., min_length=8, description="Contraseña de acceso")
    Rol: str = Field(default='C', max_length=1, description="Rol del usuario, ej: 'C' para Cliente")


class ClientRegistrationData(SQLModel):
    """
    Define los datos necesarios para crear un nuevo cliente.
    Estos son los campos que se esperan en la petición.
    """
    Nombres: str
    Apellidos: str
    DNI: str = Field(..., max_length=8, description="Documento Nacional de Identidad (8 dígitos)")
    e_mail: Optional[str] = Field(default=None, max_length=50)
    Fecha_Nac: Optional[date] = Field(default=None, description="Fecha de Nacimiento en formato YYYY-MM-DD")
    Direccion: Optional[str] = Field(default=None, max_length=100)
    CodUbigeo: Optional[str] = Field(default=None, max_length=6, description="Código de Ubigeo (6 dígitos)")
    Telefonos: Optional[str] = Field(default=None, max_length=9, description="Teléfono fijo")
    Movil: Optional[str] = Field(default=None, max_length=11, description="Teléfono móvil o celular")


class FullClientRegistration(SQLModel):
    """
    Este es el schema principal que la API espera recibir.
    Combina los datos del usuario y del cliente en un solo objeto.
    """
    user_data: UserRegistrationData
    client_data: ClientRegistrationData


# ===============================================================
# SCHEMAS PARA LA SALIDA DE DATOS (RESPONSE BODY)
# ===============================================================
# Estos definen cómo se verá la respuesta de la API cuando
# la operación sea exitosa.

class UsuarioPublic(SQLModel):
    """
    Datos públicos de un usuario (sin contraseña).
    """
    CodUsu: str
    Usuario: str
    Rol: str
    Estado: str

class ClientePublic(SQLModel):
    """
    Datos públicos de un cliente.
    """
    CodCliente: str
    Nombres: str
    Apellidos: str
    DNI: str
    e_mail: Optional[str]
    Fech_reg: date
    Estado: str

class FullClientPublic(SQLModel):
    """
    Schema de respuesta para el endpoint de registro completo.
    Devuelve los detalles del usuario y cliente recién creados.
    """
    user_details: UsuarioPublic
    client_details: ClientePublic