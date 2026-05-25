from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repository import cargo_repository
from app.schemas.cargo_schemas import CargoCreate, CargoResponse, CargoUpdate

router = APIRouter(prefix="/cargos", tags=["Cargos"])


@router.get("/", response_model=List[CargoResponse])
def listar_cargos(db: Session = Depends(get_db)):
    return cargo_repository.listar(db)


@router.get("/{id_cargo}", response_model=CargoResponse)
def buscar_cargo(id_cargo: int, db: Session = Depends(get_db)):
    cargo = cargo_repository.buscar_por_id(db, id_cargo)
    if cargo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cargo nao encontrado",
        )
    return cargo


@router.post("/", response_model=CargoResponse, status_code=status.HTTP_201_CREATED)
def criar_cargo(dados: CargoCreate, db: Session = Depends(get_db)):
    return cargo_repository.criar(db, dados)


@router.put("/{id_cargo}", response_model=CargoResponse)
def atualizar_cargo(id_cargo: int, dados: CargoUpdate, db: Session = Depends(get_db)):
    cargo = cargo_repository.buscar_por_id(db, id_cargo)
    if cargo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cargo nao encontrado",
        )
    return cargo_repository.atualizar(db, cargo, dados)


@router.delete("/{id_cargo}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_cargo(id_cargo: int, db: Session = Depends(get_db)):
    cargo = cargo_repository.buscar_por_id(db, id_cargo)
    if cargo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cargo nao encontrado",
        )
    cargo_repository.deletar(db, cargo)