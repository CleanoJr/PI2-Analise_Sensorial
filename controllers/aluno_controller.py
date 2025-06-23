from sqlalchemy import desc
from main import app
from flask import request, render_template, redirect, url_for, flash, session
from models.analise_model import Analise
from models.conexao import *
from sqlalchemy.orm import sessionmaker  # Importação da sessionmaker
from sqlalchemy.orm import joinedload

# Criando a sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Rota para listar todas as análises
@app.route("/aluno/analise/andamento", methods=['GET'])
def lista_analises_andamento():
    db = SessionLocal()
    try:
        analises = (
            db.query(Analise)
            .join(Analise.amostras)
            .options(joinedload(Analise.responsavel), joinedload(Analise.amostras))
            .group_by(Analise.id)
            .order_by(desc(Analise.id))
            .all()
        )

        # Adiciona quantidade_amostras em cada instância
        for analise in analises:
            analise.quantidade_amostras = len(analise.amostras)

        return render_template("/usuario_aluno/analise_em_andamento.html", analises=analises)
    finally:
        db.close()


@app.route("/aluno", methods=['GET'])
def aluno():
    return render_template("/aluno/painel_aluno.html")

@app.route("/aluno/dashboard", methods=['GET'])
def aluno_dashboard():
    db = SessionLocal()
    try:
        analises = (
            db.query(Analise)
            .join(Analise.amostras)
            .options(joinedload(Analise.responsavel), joinedload(Analise.amostras))
            .group_by(Analise.id)
            .order_by(desc(Analise.id))
            .all()
        )

        # Adiciona quantidade_amostras em cada instância
        for analise in analises:
            analise.quantidade_amostras = len(analise.amostras)
        return render_template("/usuario_aluno/dashboard.html", analises=analises)
    finally:
        db.close()
   

@app.route("/aluno/analise", methods=['GET'])
def aluno_analise():
    return render_template("/usuario_aluno/analise.html")

@app.route("/teste", methods=['GET'])
def teste():
    return render_template("/usuario_aluno/dashboard.html")
