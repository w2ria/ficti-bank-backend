from typing import Optional, Literal
from sqlmodel import SQLModel, Field

# ---------------------------------------------------------
# ROLES PERMITIDOS (A = Admin, E = Empleado, C = Cliente)
# ---------------------------------------------------------
RolType = Literal["A", "E", "C"]


# ---------------------------------------------------------
# BASE (Campos comunes)
# ---------------------------------------------------------
class UsuarioBase(SQLModel):
    Usuario: str
    Rol: RolType  # VALIDADO → Solo A, E o C


# ---------------------------------------------------------
# PARA CREAR USUARIO
# ---------------------------------------------------------
class UsuarioCreate(UsuarioBase):
    CodUsu: str
    Password: str = Field(..., min_length=1)


# ---------------------------------------------------------
# PARA MOSTRAR USUARIO EN RESPUESTAS
# ---------------------------------------------------------
class UsuarioPublic(UsuarioBase):
    CodUsu: str
    Estado: str


# ---------------------------------------------------------
# PARA LEER USUARIO DESDE LA BD (incluyendo hash)
# ---------------------------------------------------------
class UserFromDB(SQLModel):
    CodUsu: str
    Usuario: str
    HashedPassword: str
    Rol: RolType
    Estado: str
    email: str
    codcliente: str
    nombre_completo: str
    


# ---------------------------------------------------------
# PARA ACTUALIZAR USUARIO (parcial)
# ---------------------------------------------------------
class UsuarioUpdate(SQLModel):
    Usuario: Optional[str] = None
    Rol: Optional[RolType] = None    # VALIDADO →
    Estado: Optional[str] = None
    Password: Optional[str] = Field(default=None, min_length=1)

from sqlmodel import SQLModel, Field
from typing import Optional, Literal

class StaffRegistrationData(SQLModel):
    """
    Define los datos necesarios para registrar usuarios internos del banco (Admin o Empleado).
    """
    Nombres: str = Field(..., max_length=100, description="Nombres completos del empleado/administrador.")
    Apellidos: str = Field(..., max_length=100, description="Apellidos completos del empleado/administrador.")
    Usuario: str = Field(..., max_length=50, description="Nombre de usuario para el login.")
    Password: str = Field(..., min_length=8, description="Contraseña de acceso.")
    e_mail: str = Field(..., description="Correo electrónico.")
    
    # Restringimos el rol a solo Empleado ('E') o Administrador ('A')
    Rol: Literal['A', 'E'] = Field(
        ..., 
        description="Rol del usuario: 'A' (Administrador) o 'E' (Empleado)."
    )