from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.cargo import Cargo
from app.schemas.cargo_schemas import CargoCreate, CargoUpdate


def listar(db: Session) -> List[Cargo]:
    return db.query(Cargo).order_by(Cargo.id_cargo).all()


def buscar_por_id(db: Session, id_cargo: int) -> Optional[Cargo]:
    return db.query(Cargo).filter(Cargo.id_cargo == id_cargo).first()


def criar(db: Session, dados: CargoCreate) -> Cargo:
    novo = Cargo(**dados.model_dump())
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


def atualizar(db: Session, cargo: Cargo, dados: CargoUpdate) -> Cargo:
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(cargo, campo, valor)
    db.commit()
    db.refresh(cargo)
    return cargo


def deletar(db: Session, cargo: Cargo) -> None:
    db.delete(cargo)
    db.commit()