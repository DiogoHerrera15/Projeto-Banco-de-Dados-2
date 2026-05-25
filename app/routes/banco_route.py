from decimal import Decimal
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(prefix="/banco", tags=["Banco"])


class Reajuste(BaseModel):
    percentual: Decimal
    cargo: str


class Venda(BaseModel):
    id_cliente: int
    id_transportadora: int
    id_produto: int
    endereco_destino: str
    valor_transporte: Decimal


class UsoCashback(BaseModel):
    id_cliente: int
    valor_usado: Decimal


def rows(result):
    return [dict(r._mapping) for r in result]


#procedures
@router.post("/reajuste")
def reajuste(d: Reajuste, db: Session = Depends(get_db)):
    r = db.execute(text("CALL sp_reajuste(:p, :c)"), {"p": d.percentual, "c": d.cargo})
    out = rows(r); db.commit(); return out


@router.post("/sorteio")
def sorteio(db: Session = Depends(get_db)):
    r = db.execute(text("CALL sp_sorteio()"))
    out = rows(r); db.commit(); return out


@router.post("/venda")
def venda(d: Venda, db: Session = Depends(get_db)):
    r = db.execute(
        text("CALL sp_venda(:a, :b, :c, :e, :v)"),
        {"a": d.id_cliente, "b": d.id_transportadora, "c": d.id_produto,
         "e": d.endereco_destino, "v": d.valor_transporte},
    )
    out = rows(r); db.commit(); return out


@router.get("/estatisticas")
def estatisticas(db: Session = Depends(get_db)):
    return rows(db.execute(text("CALL sp_estatisticas()")))


#views
@router.get("/vendas-por-vendedor")
def v1(db: Session = Depends(get_db)):
    return rows(db.execute(text("SELECT * FROM vw_vendas_por_vendedor")))


@router.get("/compras-por-cliente")
def v2(db: Session = Depends(get_db)):
    return rows(db.execute(text("SELECT * FROM vw_compras_por_cliente")))


@router.get("/vendas-por-transportadora")
def v3(db: Session = Depends(get_db)):
    return rows(db.execute(text("SELECT * FROM vw_vendas_por_transportadora")))



#triggers
@router.post("/uso-cashback")
def uso_cashback(d: UsoCashback, db: Session = Depends(get_db)):
    db.execute(
        text("INSERT INTO uso_cashback (id_cliente, valor_usado) VALUES (:c, :v)"),
        {"c": d.id_cliente, "v": d.valor_usado},
    )
    db.commit()
    return {"ok": True}

@router.get("/clientes-especiais")
def ce(db: Session = Depends(get_db)):
    return rows(db.execute(text("SELECT * FROM clientes_especiais")))


@router.get("/funcionarios-especiais")
def fe(db: Session = Depends(get_db)):
    return rows(db.execute(text("SELECT * FROM funcionarios_especiais")))


@router.get("/avisos")
def avisos(db: Session = Depends(get_db)):
    return rows(db.execute(text("SELECT * FROM avisos_sistema ORDER BY data_aviso DESC")))