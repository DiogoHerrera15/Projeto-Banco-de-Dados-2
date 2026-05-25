from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.transportadora import Transportadora
from app.schemas.transportadora_schemas import TransportadoraCreate, TransportadoraUpdate


def listar(db: Session) -> List[Transportadora]:
    return db.query(Transportadora).order_by(Transportadora.id_transportadora).all()


def buscar_por_id(db: Session, id_transportadora: int) -> Optional[Transportadora]:
    return db.query(Transportadora).filter(
        Transportadora.id_transportadora == id_transportadora
    ).first()


def criar(db: Session, dados: TransportadoraCreate) -> Transportadora:
    nova = Transportadora(**dados.model_dump())
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


def atualizar(
    db: Session,
    transportadora: Transportadora,
    dados: TransportadoraUpdate,
) -> Transportadora:
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(transportadora, campo, valor)
    db.commit()
    db.refresh(transportadora)
    return transportadora


def deletar(db: Session, transportadora: Transportadora) -> None:
    db.delete(transportadora)
    db.commit()