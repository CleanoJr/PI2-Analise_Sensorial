from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.conexao import Base, engine


class Produtos(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    responsaveis_id = Column(Integer, ForeignKey('usuarios.id'))
    data = Column(String(255), nullable=False)
    justificativa = Column(String(1000), nullable=True)
    testes_realizados = Column(String(255))

    # Relacionamentos
    responsaveis = relationship("Usuario", back_populates="responsaveis_produto")
   

    def __init__(self, nome, responsaveis_id, data_cadastro, justificativa, testes_realizados,):
        self.nome = nome
        self.responsaveis_id = responsaveis_id
        self.data_cadastro = data_cadastro
        self.justificativa = justificativa
        self.testes_realizados = testes_realizados
