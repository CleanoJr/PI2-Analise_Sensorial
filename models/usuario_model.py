from sqlalchemy import Boolean, Column, Integer, String, Date
from sqlalchemy.orm import relationship
from models.conexao import Base, engine  # Certifique-se de que a conexão com o banco está correta
from models.associacoes import analise_usuario, produto_usuario

class Usuario(Base):
    __tablename__ = "usuarios"

    # Definindo a chave primária com autoincremento
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    nome = Column(String(200))
    email = Column(String(100))
    telefone = Column(String(15))
    data_nascimento = Column(Date)
    login = Column(String(200))
    senha = Column(String(15))
    tipo = Column(String(20))  # Pode ser "aluno" ou "professor"
    ativo = Column(String(10), default="Ativo")  # Mudando para String com valores "Ativo" ou "Inativo"
    analises_responsavel = relationship("Analise", back_populates="responsavel")
    responsaveis_produto = relationship("Produto", back_populates="responsaveis")
    analises = relationship(
        "Analise",
        secondary=analise_usuario,
        back_populates="participantes"
    )

    produtos = relationship(
        "Produto",
        secondary=produto_usuario,
        back_populates="responsaveis"
    )


    def __init__(self, nome, email, telefone, data_nascimento, login, senha, tipo, ativo="Ativo"):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.data_nascimento = data_nascimento
        self.login = login
        self.senha = senha
        self.tipo = tipo
        self.ativo = ativo