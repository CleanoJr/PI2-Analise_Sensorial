from sqlalchemy import Column, Integer, String
from models.conexao import Base, engine

class Testador(Base):
    __tablename__ = "testadores"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    faixa_etaria = Column(String(255), nullable=False)
    genero = Column(String(255), nullable=False)
   
