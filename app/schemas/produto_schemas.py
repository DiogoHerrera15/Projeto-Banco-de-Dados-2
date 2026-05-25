from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    descricao: str = Field(..., min_length=1)
    quantidade_estoque: int = Field(..., ge=0)
    valor: Decimal = Field(..., ge=0)
    observacoes: Optional[str] = None
    id_vendedor: int


class ProdutoCreate(ProdutoBase):
    pass


class ProdutoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=100)
    descricao: Optional[str] = Field(None, min_length=1)
    quantidade_estoque: Optional[int] = Field(None, ge=0)
    valor: Optional[Decimal] = Field(None, ge=0)
    observacoes: Optional[str] = None
    id_vendedor: Optional[int] = None


class ProdutoResponse(ProdutoBase):
    id_produto: int

    model_config = ConfigDict(from_attributes=True)