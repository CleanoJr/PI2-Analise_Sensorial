from main import app
from flask import request, render_template, redirect, url_for, flash, session
from models.analise_model import Analise
from models.conexao import *
from sqlalchemy.orm import sessionmaker  # Importação da sessionmaker

# Criando a sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Rota para listar todas as análises
@app.route("/analise/list", methods=['GET'])
def lista_analises():
    db = SessionLocal()
    analises = db.query(Analise).all()
    db.close()
    return render_template("/analises/list_analises.html", analises=analises)

# Rota para exibir fomrulário
@app.route("/analise/cadastro", methods=['GET'])
def form_analise():
    return render_template("/analises/nova_analise.html")

# Rota para criar nova análise
@app.route("/analise/nova", methods=['POST'])
def nova_analise():
    if request.method == 'POST':
        nome = request.form['nome']
        responsavel = request.form['responsavel']
        data = request.form['data']
        status = request.form['status']
        tipo_avaliacao = request.form['tipo']
        intencao_compra = request.form['intencao']
        justificativa = request.form['justificativa']

        nova_analise = Analise(
            nome=nome,
            responsavel=responsavel,
            data=data,
            status=status,
            tipo_avaliacao=tipo_avaliacao,
            intencao_compra=intencao_compra,
            justificativa=justificativa
        )

        db = SessionLocal()
        db.add(nova_analise)
        db.commit()
        db.close()

        flash("Análise criada com sucesso!", "success")
        return redirect(url_for('lista_analises'))

    return render_template("/analises/nova_analise.html")

# Rota para exibir detalhes de uma análise
@app.route("/analise/<int:id>/detalhes", methods=['GET'])
def detalhes_analise(id):
    db = SessionLocal()
    analise = db.query(Analise).filter_by(id=id).first()
    if not analise:
        db.close()
        flash("Análise não encontrada!", "error")
        return redirect(url_for('lista_analises'))
    amostras = analise.amostras
    db.close()
    return render_template("/analises/detalhe_analise.html", analise=analise, amostras=amostras)

# Rota para exibir formulário de edição
@app.route("/analise/<int:id>/editar", methods=['GET'])
def form_editar_analise(id):
    db = SessionLocal()
    analise = db.query(Analise).filter_by(id=id).first()
    if not analise:
        db.close()
        flash("Análise não encontrada!", "error")
        return redirect(url_for('lista_analises'))
    db.close()
    return render_template("/analises/edit_analise.html", analise=analise)

# Rota para atualizar uma análise
@app.route("/analise/<int:id>/editar", methods=['POST'])
def editar_analise(id):
    db = SessionLocal()
    analise = db.query(Analise).filter_by(id=id).first()
    if not analise:
        db.close()
        flash("Análise não encontrada!", "error")
        return redirect(url_for('lista_analises'))

    analise.nome = request.form['nome']
    analise.responsavel = request.form['responsavel']
    analise.data = request.form['data']
    analise.status = request.form['status']
    analise.tipo_avaliacao = request.form['tipo']
    analise.intencao_compra = request.form['intencao']
    analise.justificativa = request.form['justificativa']

    db.commit()
    db.close()

    flash("Análise atualizada com sucesso!", "success")
    return redirect(url_for('lista_analises'))

# Rota para excluir uma análise
@app.route("/analise/<int:id>/excluir", methods=['GET'])
def excluir_analise(id):
    db = SessionLocal()
    analise = db.query(Analise).filter_by(id=id).first()
    if not analise:
        db.close()
        flash("Análise não encontrada!", "error")
        return redirect(url_for('lista_analises'))

    db.delete(analise)
    db.commit()
    db.close()

    flash("Análise excluída com sucesso!", "success")
    return redirect(url_for('lista_analises'))