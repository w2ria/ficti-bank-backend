from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

# Forward declaration para evitar importación circular con Cliente y Cuenta
class Cliente(SQLModel):
    pass
class Cuenta(SQLModel):
    pass

class Usuario(SQLModel, table=True):
    __tablename__ = "T_Usuario"

    CodUsu: str = Field(primary_key=True, max_length=10)
    Usuario: Optional[str] = Field(default=None, max_length=100, unique=True, index=True)
    Rol: Optional[str] = Field(default=None, max_length=1)
    Estado: Optional[str] = Field(default=None, max_length=1, foreign_key="T_Estado.Estado")
    HashedPassword: str = Field(max_length=255)

    # Relaciones: Un usuario puede registrar muchos clientes y cuentas
    clientes_registrados: List["Cliente"] = Relationship(back_populates="usuario_registrador")
    cuentas_registradas: List["Cuenta"] = Relationship(back_populates="usuario_registrador")