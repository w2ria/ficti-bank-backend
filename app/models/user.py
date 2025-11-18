from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel

class Usuario(SQLModel, table=True):
    __tablename__ = "t_usuario"

    CodUsu: str = Field(primary_key=True, max_length=10)
    Usuario: Optional[str] = Field(default=None, max_length=100, unique=True, index=True)
    Rol: Optional[str] = Field(default=None, max_length=1)
    Estado: Optional[str] = Field(default=None, max_length=1, foreign_key="t_estado.Estado")
    HashedPassword: str = Field(max_length=255)

    # 🆕 Campos para control de login
    IntentosFallidos: int = Field(default=0)
    UltimoIntento: Optional[datetime] = Field(default=None)
