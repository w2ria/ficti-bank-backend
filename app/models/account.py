from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import date
from decimal import Decimal
from app.models.user import Usuario
from app.models.client import Cliente


class Cuenta(SQLModel, table=True):
    __tablename__ = "T_Cuentas"
    
    NroCta: str = Field(primary_key=True, max_length=20)
    TipoCta: Optional[str] = Field(default=None, max_length=2, foreign_key="T_TipoCuentas.TipoCta")
    CodCliente: Optional[str] = Field(default=None, max_length=10, foreign_key="T_Cliente.CodCliente")
    Moneda: Optional[str] = Field(default=None, max_length=2)
    Fech_Apert: Optional[date] = None
    SaldAct: Optional[Decimal] = Field(default=0.0, max_digits=10, decimal_places=2)
    Estado: Optional[str] = Field(default=None, max_length=1, foreign_key="T_Estado.Estado")

    # Foreign Key al usuario que la registró
    CodUsu: Optional[str] = Field(default=None, foreign_key="T_Usuario.CodUsu")

    # Relaciones
    cliente: Optional[Cliente] = Relationship(back_populates="cuentas")
    usuario_registrador: Optional[Usuario] = Relationship(back_populates="cuentas_registradas")


class Movimiento(SQLModel, table=True):
    __tablename__ = "T_Movimientos"
    
    # Clave primaria compuesta
    NroCta: str = Field(primary_key=True, max_length=20, foreign_key="T_Cuentas.NroCta")
    NroOperNumber: int = Field(primary_key=True)
    
    Fech_Ope: Optional[date] = None
    CodUsu: Optional[str] = Field(default=None, max_length=10, foreign_key="T_Usuario.CodUsu")
    TipoMov: Optional[str] = Field(default=None, max_length=2, foreign_key="T_TipoMovi.TipoMov")
    MonOpe: Optional[Decimal] = Field(default=None, max_digits=10, decimal_places=2)
    Estado: Optional[str] = Field(default=None, max_length=1, foreign_key="T_Estado.Estado")
