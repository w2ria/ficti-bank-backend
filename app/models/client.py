from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import date
from app.models.user import Usuario


# Forward declaration
class Cuenta(SQLModel):
    pass


class Cliente(SQLModel, table=True):
    __tablename__ = "T_Cliente"

    CodCliente: str = Field(primary_key=True, max_length=10)
    Apellidos: Optional[str] = Field(default=None, max_length=100)
    Nombres: Optional[str] = Field(default=None, max_length=100)
    DNI: Optional[str] = Field(default=None, max_length=8)
    Fecha_Nac: Optional[date] = None
    Direccion: Optional[str] = Field(default=None, max_length=100)
    CodUbigeo: Optional[str] = Field(default=None, max_length=6, foreign_key="T_Ubigeo.CodUbigeo")
    Telefonos: Optional[str] = Field(default=None, max_length=9)
    Movil: Optional[str] = Field(default=None, max_length=11)
    e_mail: Optional[str] = Field(default=None, max_length=50)
    Fech_reg: Optional[date] = None
    Estado: Optional[str] = Field(default=None, max_length=1, foreign_key="T_Estado.Estado")
    
    # Foreign Key al usuario que lo registró
    CodUsu: Optional[str] = Field(default=None, foreign_key="T_Usuario.CodUsu")

    # Relaciones
    usuario_registrador: Optional[Usuario] = Relationship(back_populates="clientes_registrados")
    cuentas: List["Cuenta"] = Relationship(back_populates="cliente")
