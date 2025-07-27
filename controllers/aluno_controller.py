from sqlalchemy import desc
from main import app
from flask import request, render_template, redirect, url_for, flash, session
from models.analise_model import *
from models.amostra_model import *
from models.avaliacao_modal import *
from models.conexao import *
from sqlalchemy.orm import sessionmaker, joinedload
from collections import defaultdict

# Criando a sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Lista análises em andamento com suas amostras e quantidade de avaliações feitas
@app.route("/aluno/analise/andamento", methods=['GET'])
def lista_analises_andamento():
    db = SessionLocal()
    try:
        analises = (
            db.query(Analise)
            .join(Analise.amostras)
            .filter(Analise.status == 'Em andamento')
            .options(joinedload(Analise.responsavel), joinedload(Analise.amostras))
            .order_by(desc(Analise.id))
            .all()
        )

        for analise in analises:
            analise.quantidade_amostras = len(analise.amostras)

            testadores_unicos = (
                db.query(Avaliacao.testador_id)
                .join(Avaliacao.amostra)
                .filter(Amostra.analise_id == analise.id, Avaliacao.testador_id != None)
                .distinct()
                .count()
            )

            analise.quantidade_avaliacoes = testadores_unicos

        return render_template("/usuario_aluno/analise_em_andamento.html", analises=analises)
    finally:
        db.close()


# Página inicial do aluno
@app.route("/aluno", methods=['GET'])
def aluno():
    return render_template("/aluno/painel_aluno.html")

# Dashboard do aluno com lista de análises
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

        for analise in analises:
            analise.quantidade_amostras = len(analise.amostras)
        return render_template("/usuario_aluno/dashboard.html", analises=analises)
    finally:
        db.close()

# Rota simples para tela de análise do aluno
@app.route("/aluno/analise", methods=['GET'])
def aluno_analise():
    return render_template("/usuario_aluno/analise.html")

# Rota de teste que aponta para dashboard
@app.route("/teste", methods=['GET'])
def teste():
    return render_template("/usuario_aluno/dashboard.html")