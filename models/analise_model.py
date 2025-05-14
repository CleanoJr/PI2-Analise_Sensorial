from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models.conexao import Base, engine
from models.associacoes import analise_usuario


class Analise(Base):
    __tablename__ = "analises"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    responsavel = Column(String(255), nullable=False)
    data = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False)
    tipo_avaliacao = Column(String(255), nullable=False)
    justificativa = Column(String(1000), nullable=True)
    amostras = relationship("Amostra", backref="analise", cascade="all, delete-orphan", lazy=True)
    participantes = relationship(
        "Usuario",
        secondary=analise_usuario,
        back_populates="analises"
    )

    def __init__(self, nome, responsavel, data, status, tipo_avaliacao, justificativa=None):
        self.nome = nome
        self.responsavel = responsavel
        self.data = data
        self.status = status
        self.tipo_avaliacao = tipo_avaliacao
        self.justificativa = justificativa