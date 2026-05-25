from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repository import transportadora_repository
from app.schemas.transportadora_schemas import (
    TransportadoraCreate,
    TransportadoraResponse,
    TransportadoraUpdate,
)

router = APIRouter(prefix="/transportadoras", tags=["Transportadoras"])


@router.get("/", response_model=List[TransportadoraResponse])
def listar_transportadoras(db: Session = Depends(get_db)):
    return transportadora_repository.listar(db)


@router.get("/{id_transportadora}", response_model=TransportadoraResponse)
def buscar_transportadora(id_transportadora: int, db: Session = Depends(get_db)):
    transportadora = transportadora_repository.buscar_por_id(db, id_transportadora)
    if transportadora is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transportadora nao encontrada",
        )
    return transportadora


@router.post(
    "/",
    response_model=TransportadoraResponse,
    status_code=status.HTTP_201_CREATED,
)
def criar_transportadora(
    dados: TransportadoraCreate,
    db: Session = Depends(get_db),
):
    return transportadora_repository.criar(db, dados)


@router.put("/{id_transportadora}", response_model=TransportadoraResponse)
def atualizar_transportadora(
    id_transportadora: int,
    dados: TransportadoraUpdate,
    db: Session = Depends(get_db),
):
    transportadora = transportadora_repository.buscar_por_id(db, id_transportadora)
    if transportadora is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transportadora nao encontrada",
        )
    return transportadora_repository.atualizar(db, transportadora, dados)


@router.delete("/{id_transportadora}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_transportadora(
    id_transportadora: int,
    db: Session = Depends(get_db),
):
    transportadora = transportadora_repository.buscar_por_id(db, id_transportadora)
    if transportadora is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Transportadora nao encontrada",
        )
    transportadora_repository.deletar(db, transportadora)