from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class TransportadoraBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    cidade: str = Field(..., min_length=1, max_length=100)


class TransportadoraCreate(TransportadoraBase):
    pass


class TransportadoraUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=100)
    cidade: Optional[str] = Field(None, min_length=1, max_length=100)


class TransportadoraResponse(TransportadoraBase):
    id_transportadora: int

    model_config = ConfigDict(from_attributes=True)