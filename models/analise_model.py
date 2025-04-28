from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.conexao import Base, engine

class Analise(Base):
    __tablename__ = "analises"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    responsavel = Column(String(255), nullable=False)
    data = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False)
    tipo_avaliacao = Column(String(255), nullable=False)
    intencao_compra = Column(String(255), nullable=False)
    justificativa = Column(String(1000), nullable=True)
    amostras = relationship("Amostra", backref="analise", cascade="all, delete-orphan", lazy=True)

    def __init__(self, nome, responsavel, data, status, tipo_avaliacao, intencao_compra, justificativa=None):
        self.nome = nome
        self.responsavel = responsavel
        self.data = data
        self.status = status
        self.tipo_avaliacao = tipo_avaliacao
        self.intencao_compra = intencao_compra
        self.justificativa = justificativa

# Criando a tabela no banco de dados, caso não exista
Base.metadata.create_all(bind=engine)