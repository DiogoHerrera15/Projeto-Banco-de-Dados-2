from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CargoBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=100)
    descricao: Optional[str] = None


class CargoCreate(CargoBase):
    pass


class CargoUpdate(BaseModel):
    nome: Optional[str] = Field(None, min_length=1, max_length=100)
    descricao: Optional[str] = None


class CargoResponse(CargoBase):
    id_cargo: int

    model_config = ConfigDict(from_attributes=True)