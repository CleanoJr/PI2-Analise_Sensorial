from sqlalchemy import Column, Integer, String
from models.conexao import Base, engine


class Avaliador(Base):
    __tablename__ = 'avaliadores'

    id = Column(Integer, primary_key=True , autoincrement=True)
    nome = Column(String(200), nullable=False)
    email = Column(String(15), nullable=False)
    genero = Column(String(20), nullable=False)
    idade = Column(Integer(20), nullable=False)
   
   
    
    def __init__(self, nome, email,genero,idade):
        self.nome = nome
        self.email = email
        self.genero= genero
        self.idade = idade
      