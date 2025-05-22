from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.conexao import Base, engine
from models.associacoes import analise_usuario


class Analise(Base):
    __tablename__ = "analises"

    id = Column(Integer, primary_key=True, autoincrement=True)
    produto = Column(String(255), nullable=False)
    responsavel_id = Column(Integer, ForeignKey('usuarios.id'))
    data = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False)
    teste = Column(String(255), nullable=False)
    justificativa = Column(String(1000), nullable=True)

    # Relacionamentos
    responsavel = relationship("Usuario", back_populates="analises_responsavel")
    amostras = relationship("Amostra", backref="analise", cascade="all, delete-orphan", lazy=True)
    participantes = relationship(
        "Usuario",
        secondary=analise_usuario,
        back_populates="analises"
    )

    def __init__(self, produto, responsavel_id, data, status, teste, justificativa=None):
        self.produto = produto
        self.responsavel_id = responsavel_id
        self.data = data
        self.status = status
        self.teste = teste
        self.justificativa = justificativa