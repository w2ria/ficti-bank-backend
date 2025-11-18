from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

class EmbargoCreate(BaseModel):
    """
    Schema del BODY para registrar un embargo.
    """
    NroCta: str = Field(..., max_length=20, description="Número de cuenta a embargar")
    TipoEmbargo: str = Field(..., max_length=1, pattern="^[TP]$", description="T = Total, P = Parcial")
    MontoEmbargado: Decimal = Field(..., gt=0, description="Monto a embargar")
    Observaciones: Optional[str] = Field(default=None, description="Notas adicionales")
    CodUsu: str = Field(..., max_length=10, description="Usuario que registra el embargo")
