from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.produto import Produto
from app.schemas.produto_schemas import ProdutoCreate, ProdutoUpdate


def listar(db: Session) -> List[Produto]:
    return db.query(Produto).order_by(Produto.id_produto).all()


def buscar_por_id(db: Session, id_produto: int) -> Optional[Produto]:
    return db.query(Produto).filter(Produto.id_produto == id_produto).first()


def criar(db: Session, dados: ProdutoCreate) -> Produto:
    novo = Produto(**dados.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


def atualizar(db: Session, produto: Produto, dados: ProdutoUpdate) -> Produto:
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(produto, campo, valor)
    db.commit()
    db.refresh(produto)
    return produto


def deletar(db: Session, produto: Produto) -> None:
    db.delete(produto)
    db.commit()