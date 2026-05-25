from sqlalchemy import Column, Integer, String

from app.database import Base


class Transportadora(Base):
    __tablename__ = "transportadoras"

    id_transportadora = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
