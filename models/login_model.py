from sqlalchemy import Boolean, Column, Integer, String, Date
from sqlalchemy.orm import relationship
from models.conexao import Base, engine  # Certifique-se de que a conexão com o banco está correta
from models.associacoes import analise_usuario

class Login(Base):
    __tablename__ = "logins"

    # Definindo a chave primária com autoincremento
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    login = Column(String(200))
    senha = Column(String(15))
    ativo = Column(String(10), default="Ativo")  # Mudando para String com valores "Ativo" ou "Inativo"
    
    analises = relationship(
        "Analise",
        secondary=analise_usuario,
        back_populates="participantes"
    )

    def __init__(self, login, senha, ativo="Ativo"):
        self.login = login
        self.senha = senha
        self.ativo = ativo