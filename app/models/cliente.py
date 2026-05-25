from sqlalchemy import Column, Date, Integer, String

from app.database import Base


class Cliente(Base):
    __tablename__ = "clientes"

    id_cliente = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    idade = Column(Integer, nullable=False)
    sexo = Column(String(20), nullable=False)
    data_nascimento = Column(Date, nullable=False)
