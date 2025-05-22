from sqlalchemy import Column, Integer, String, ForeignKey
from models.conexao import Base, engine

class Avaliacao(Base):
    __tablename__ = "avaliacoes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(Integer,nullable=False)
    status = Column(String(255), nullable=False)
    amostra_id = Column(Integer, ForeignKey("amostras.id"), nullable=False)
    testador_id = Column(Integer, ForeignKey("testadores.id"), nullable=True)

    