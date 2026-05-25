from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
 
from app.database import Base
 
 
class Cargo(Base):
    __tablename__ = "cargos"
 
    id_cargo = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=True)
 
    vendedores = relationship("Vendedor", back_populates="cargo")   
