from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repository import produto_repository, vendedor_repository
from app.schemas.produto_schemas import ProdutoCreate, ProdutoResponse, ProdutoUpdate

router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.get("/", response_model=List[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    return produto_repository.listar(db)


@router.get("/{id_produto}", response_model=ProdutoResponse)
def buscar_produto(id_produto: int, db: Session = Depends(get_db)):
    produto = produto_repository.buscar_por_id(db, id_produto)
    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto nao encontrado",
        )
    return produto


@router.post("/", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
def criar_produto(dados: ProdutoCreate, db: Session = Depends(get_db)):
    if vendedor_repository.buscar_por_id(db, dados.id_vendedor) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Vendedor com id {dados.id_vendedor} nao existe",
        )
    return produto_repository.criar(db, dados)


@router.put("/{id_produto}", response_model=ProdutoResponse)
def atualizar_produto(
    id_produto: int,
    dados: ProdutoUpdate,
    db: Session = Depends(get_db),
):
    produto = produto_repository.buscar_por_id(db, id_produto)
    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto nao encontrado",
        )
    if dados.id_vendedor is not None:
        if vendedor_repository.buscar_por_id(db, dados.id_vendedor) is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Vendedor com id {dados.id_vendedor} nao existe",
            )
    return produto_repository.atualizar(db, produto, dados)


@router.delete("/{id_produto}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_produto(id_produto: int, db: Session = Depends(get_db)):
    produto = produto_repository.buscar_por_id(db, id_produto)
    if produto is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto nao encontrado",
        )
    produto_repository.deletar(db, produto)