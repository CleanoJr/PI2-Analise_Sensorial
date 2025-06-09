from sqlalchemy import Column, Integer, String
from models.conexao import Base, engine


class Avaliador(Base):
    __tablename__ = 'avaliadores'

    id = Column(Integer, primary_key=True , autoincrement=True)
    nome = Column(String(200), nullable=False)
    email = Column(String(15), nullable=False)
    genero = Column(String(20), nullable=False)
    faixa_etaria = Column(Integer(20), nullable=False)
   
   
    
    def __init__(self, nome, email,genero,faixa_etaria):
        self.nome = nome
        self.email = email
        self.genero= genero
        self.faixa_etaria = faixa_etaria
      