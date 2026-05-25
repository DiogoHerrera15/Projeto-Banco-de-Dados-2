from sqlalchemy import Column, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import relationship

from app.database import Base


class Vendedor(Base):
    __tablename__ = "Vendedores"

    id_vendedor = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    causa_social = Column(String(150), nullable=False)
    tipo = Column(String(50), nullable=False)
    nota_media = Column(Numeric(3, 2), default=0.00)
    salario = Column(Numeric(10, 2), nullable=False)
    id_cargo = Column(
        Integer,
        ForeignKey("cargos.id_cargo"),
        nullable=False,
    )

    cargo = relationship("Cargo", back_populates="vendedores")
    produtos = relationship("Produto", back_populates="vendedor")
