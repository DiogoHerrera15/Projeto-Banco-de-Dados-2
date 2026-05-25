from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ClienteBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    idade: int = Field(..., ge=0)
    sexo: str = Field(..., min_length=1, max_length=20)
    data_nascimento: date


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=100)
    idade: Optional[int] = Field(None, ge=0)
    sexo: Optional[str] = Field(None, min_length=1, max_length=20)
    data_nascimento: Optional[date] = None


class ClienteResponse(ClienteBase):
    id_cliente: int

    model_config = ConfigDict(from_attributes=True)