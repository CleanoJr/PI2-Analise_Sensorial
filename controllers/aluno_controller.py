from sqlalchemy import desc
from main import app
from flask import redirect
from flask import request, render_template, redirect, url_for, flash, session
from models.analise_model import *
from models.amostra_model import *
from models.avaliacao_modal import *
from models.conexao import *
from sqlalchemy.orm import sessionmaker  # Importação da sessionmaker
from sqlalchemy.orm import joinedload
from collections import defaultdict

# Criando a sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Rota para listar todas as análises
@app.route("/aluno/analise/andamento", methods=['GET'])
def lista_analises_andamento():
    db = SessionLocal()
    try:
        analises = (
            db.query(Analise)
            .join(Analise.amostras)  # Garante que tenha pelo menos uma amostra vinculada
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


@app.route("/aluno", methods=['GET'])
def aluno():
    return render_template("/aluno/painel_aluno.html")

@app.route("/aluno/dashboard", methods=['GET'])
def aluno_dashboard():
     return redirect(url_for('dashboard'))
    
    #db = SessionLocal()
    #try:
        #analises = (
            #db.query(Analise)
            #.join(Analise.amostras)
            #.options(joinedload(Analise.responsavel), #joinedload(Analise.amostras))
            #.group_by(Analise.id)
            #.order_by(desc(Analise.id))
            #.all()
        #)

        # Adiciona quantidade_amostras em cada instância
        #for analise in analises:
            #analise.quantidade_amostras = len(analise.amostras)
        #return render_template("/usuario_aluno/dashboard_atualizado.html", analises=analises)
    #finally:
        #db.close()
   

@app.route("/aluno/analise", methods=['GET'])
def aluno_analise():
    return render_template("/usuario_aluno/analise.html")

@app.route("/teste", methods=['GET'])
def teste():
    return render_template("/usuario_aluno/dashboard_atualizado.html")
