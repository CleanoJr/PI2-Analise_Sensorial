from sqlalchemy import Column, Integer, String, ForeignKey
from models.conexao import Base, engine

class Amostra(Base):
    __tablename__ = "amostras"

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(255), nullable=False)
    analise_id = Column(Integer, ForeignKey("analises.id"), nullable=False)

    def __init__(self, descricao, analise_id):
        self.descricao = descricao
        self.analise_id = analise_id