from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repository import cargo_repository, vendedor_repository
from app.schemas.vendedor_schemas import VendedorCreate, VendedorResponse, VendedorUpdate

router = APIRouter(prefix="/vendedores", tags=["Vendedores"])


@router.get("/", response_model=List[VendedorResponse])
def listar_vendedores(db: Session = Depends(get_db)):
    return vendedor_repository.listar(db)


@router.get("/{id_vendedor}", response_model=VendedorResponse)
def buscar_vendedor(id_vendedor: int, db: Session = Depends(get_db)):
    vendedor = vendedor_repository.buscar_por_id(db, id_vendedor)
    if vendedor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor nao encontrado",
        )
    return vendedor


@router.post("/", response_model=VendedorResponse, status_code=status.HTTP_201_CREATED)
def criar_vendedor(dados: VendedorCreate, db: Session = Depends(get_db)):
    if cargo_repository.buscar_por_id(db, dados.id_cargo) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cargo com id {dados.id_cargo} nao existe",
        )
    return vendedor_repository.criar(db, dados)


@router.put("/{id_vendedor}", response_model=VendedorResponse)
def atualizar_vendedor(
    id_vendedor: int,
    dados: VendedorUpdate,
    db: Session = Depends(get_db),
):
    vendedor = vendedor_repository.buscar_por_id(db, id_vendedor)
    if vendedor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor nao encontrado",
        )
    if dados.id_cargo is not None:
        if cargo_repository.buscar_por_id(db, dados.id_cargo) is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Cargo com id {dados.id_cargo} nao existe",
            )
    return vendedor_repository.atualizar(db, vendedor, dados)


@router.delete("/{id_vendedor}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_vendedor(id_vendedor: int, db: Session = Depends(get_db)):
    vendedor = vendedor_repository.buscar_por_id(db, id_vendedor)
    if vendedor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendedor nao encontrado",
        )
    vendedor_repository.deletar(db, vendedor)