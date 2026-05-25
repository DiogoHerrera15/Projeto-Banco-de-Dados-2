from sqlalchemy import Column, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Produto(Base):
    __tablename__ = "produtos"

    id_produto = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=False)
    quantidade_estoque = Column(Integer, nullable=False)
    valor = Column(Numeric(10, 2), nullable=False)
    observacoes = Column(Text, nullable=True)
    id_vendedor = Column(
        Integer,
        ForeignKey("vendedores.id_vendedor"),
        nullable=False,
    )

    vendedor = relationship("Vendedor", back_populates="produtos")
