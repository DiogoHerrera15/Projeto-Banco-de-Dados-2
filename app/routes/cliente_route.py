from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repository import cliente_repository
from app.schemas.clientes_schemas import ClienteCreate, ClienteResponse, ClienteUpdate

router = APIRouter(prefix="/clientes", tags=["Clientes"])


@router.get("/", response_model=List[ClienteResponse])
def listar_clientes(db: Session = Depends(get_db)):
    return cliente_repository.listar(db)


@router.get("/{id_cliente}", response_model=ClienteResponse)
def buscar_cliente(id_cliente: int, db: Session = Depends(get_db)):
    cliente = cliente_repository.buscar_por_id(db, id_cliente)
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente nao encontrado",
        )
    return cliente


@router.post("/", response_model=ClienteResponse, status_code=status.HTTP_201_CREATED)
def criar_cliente(dados: ClienteCreate, db: Session = Depends(get_db)):
    return cliente_repository.criar(db, dados)


@router.put("/{id_cliente}", response_model=ClienteResponse)
def atualizar_cliente(id_cliente: int, dados: ClienteUpdate, db: Session = Depends(get_db)):
    cliente = cliente_repository.buscar_por_id(db, id_cliente)
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente nao encontrado",
        )
    return cliente_repository.atualizar(db, cliente, dados)


@router.delete("/{id_cliente}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_cliente(id_cliente: int, db: Session = Depends(get_db)):
    cliente = cliente_repository.buscar_por_id(db, id_cliente)
    if cliente is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cliente nao encontrado",
        )
    cliente_repository.deletar(db, cliente)