from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.cliente import Cliente
from app.schemas.clientes_schemas import ClienteCreate, ClienteUpdate


def listar(db: Session) -> List[Cliente]:
    return db.query(Cliente).order_by(Cliente.id_cliente).all()


def buscar_por_id(db: Session, id_cliente: int) -> Optional[Cliente]:
    return db.query(Cliente).filter(Cliente.id_cliente == id_cliente).first()


def criar(db: Session, dados: ClienteCreate) -> Cliente:
    novo = Cliente(**dados.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


def atualizar(db: Session, cliente: Cliente, dados: ClienteUpdate) -> Cliente:
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(cliente, campo, valor)
    db.commit()
    db.refresh(cliente)
    return cliente


def deletar(db: Session, cliente: Cliente) -> None:
    db.delete(cliente)
    db.commit()