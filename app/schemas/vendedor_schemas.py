from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class VendedorBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    causa_social: str = Field(..., min_length=1, max_length=150)
    tipo: str = Field(..., min_length=1, max_length=50)
    nota_media: Decimal = Field(default=Decimal("0.00"), ge=0, le=5)
    salario: Decimal = Field(..., ge=0)
    id_cargo: int


class VendedorCreate(VendedorBase):
    pass


class VendedorUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=100)
    causa_social: Optional[str] = Field(None, min_length=1, max_length=150)
    tipo: Optional[str] = Field(None, min_length=1, max_length=50)
    nota_media: Optional[Decimal] = Field(None, ge=0, le=5)
    salario: Optional[Decimal] = Field(None, ge=0)
    id_cargo: Optional[int] = None


class VendedorResponse(VendedorBase):
    id_vendedor: int

    model_config = ConfigDict(from_attributes=True)