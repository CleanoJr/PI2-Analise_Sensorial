from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from models.conexao import Base, engine
from models.associacoes import produto_usuario


class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    responsaveis_id = Column(Integer, ForeignKey('usuarios.id'))
    data_cadastro = Column(DateTime(255), default=datetime.now)
    justificativa = Column(String(1000), nullable=True)
    testes_realizados = Column(String(255), nullable=True)

    # Relacionamentos
    responsaveis = relationship(
    "Usuario",
    secondary=produto_usuario,
    back_populates="produtos"
)
   

    def __init__(self, nome, responsaveis_id, justificativa):
        self.nome = nome
        self.responsaveis_id = responsaveis_id
        self.justificativa = justificativa
        # self.testes_realizados = testes_realizados

