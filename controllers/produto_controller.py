from main import app
from flask import request, render_template, redirect, url_for, flash, session
from models.analise_model import Analise
from models.produto_model import Produto
from models.usuario_model import Usuario
from pdf_dos_relatorios.relatorios_controller import *
from models.conexao import *
from sqlalchemy.orm import sessionmaker  # Importação da sessionmaker
from sqlalchemy.orm import joinedload
from sqlalchemy import select

from sqlalchemy import desc  # importa a função desc descending da biblioteca sqlalchemy

# Criando a sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Rota para listar todas as análises
@app.route("/produto/list", methods=['GET'])
def lista_produtos():
    db = SessionLocal()
    try:
        produtos = db.query(Produto).options(joinedload(Produto.responsaveis)).order_by(desc(Produto.id)).all()
        # Força o acesso ao relacionamento para garantir que esteja carregado
        for produto in produtos:
            _ = produto.responsaveis
        return render_template("/produtos/list_produtos.html", produtos=produtos)
    finally:
        db.close()

# Rota para exibir formulário de cadastro
@app.route("/produtos/cadastro", methods=['GET'])
def form_produto():
    db = SessionLocal()
    # Busca apenas professores ativos
    professores = db.query(Usuario).filter_by(tipo="professor", ativo="Ativo").all()
    db.close()
    return render_template("/produtos/novo_produto.html", professores=professores)

# Rota para criar nova análise
@app.route("/produtos/novo", methods=['POST'])
def novo_produto():
    if request.method == 'POST':
        produto = request.form['produto']
        responsavel_id = request.form['responsavel']
        justificativa = request.form['justificativa']


        db = SessionLocal()
        # Valida o professor selecionado
        responsavel = db.query(Usuario).filter_by(id=responsavel_id, tipo="professor", ativo="Ativo").first()
        if not responsavel:
            db.close()
            flash("Professor inválido!", "error")
            return redirect(url_for('form_produto'))

        novo_produto = Produto(
            nome=produto,
            responsaveis_id=responsavel_id,
            justificativa=justificativa

        )

        db.add(novo_produto)
        db.commit()
        db.close()

        flash("Produto cadastrado com sucesso!", "success")
        return redirect(url_for('lista_produtos'))

    return render_template("/produtos/novo_produto.html")

# Rota para exibir detalhes de uma análise
@app.route("/produtos/<int:id>/detalhes", methods=['GET'])
def detalhes_produto(id):
    db = SessionLocal()
    try:
        produto = db.query(Produto).options(
            joinedload(Produto.participantes),
            joinedload(Produto.responsavel)
        ).filter_by(id=id).first()
        
        if not analise:
            flash("Análise não encontrada!", "error")
            return redirect(url_for('lista_analises'))
        
        amostras = analise.amostras
        usuarios = db.query(Usuario).filter_by(ativo="Ativo").all()
        
        return render_template(
            "/produtos/detalhe_analise.html",
            analise=analise,
            amostras=amostras,
            usuarios=usuarios
        )
    finally:
        db.close()

# Rota para exibir formulário de edição
@app.route("/produtos/<int:id>/editar", methods=['GET'])
def form_editar_produto(id):
    db = SessionLocal()
    produto = db.query(Produto).filter_by(id=id).first()
    professores = db.query(Usuario).filter_by(tipo="professor", ativo="Ativo").all()
    if not produto:
        db.close()
        flash("Produto não encontrado!", "error")
        return redirect(url_for('lista_produtos'))
    db.close()
    return render_template("/produtos/edit_produto.html", produto=produto, professores=professores)

# Rota para atualizar uma análise
@app.route("/produtos/<int:id>/editar", methods=['POST'])
def editar_produto(id):
    db = SessionLocal()
    produto = db.query(Produto).filter_by(id=id).first()
    if not produto:
        db.close()
        flash("Produto não encontrado!", "error")
        return redirect(url_for('lista_produtos'))

    responsavel_id = request.form['responsavel']
    # Valida o professor selecionado
    responsavel = db.query(Usuario).filter_by(id=responsavel_id, tipo="professor", ativo="Ativo").first()
    if not responsavel:
        db.close()
        flash("Professor inválido!", "error")
        return redirect(url_for('form_editar_produto', id=id))

    produto.nome = request.form['produto']
    produto.responsaveis_id = responsavel_id
    produto.justificativa = request.form['justificativa']

    db.commit()
    db.close()

    flash("Produto atualizado com sucesso!", "success")
    return redirect(url_for('lista_produtos'))

# Rota para excluir uma análise
@app.route("/produtos/<int:id>/excluir", methods=['GET'])
def excluir_produto(id):
    db = SessionLocal()
    produto = db.query(Produto).filter_by(id=id).first()
    if not produto:
        db.close()
        flash("Produto não encontrado!", "error")
        return redirect(url_for('lista_produtos'))

    db.delete(produto)
    db.commit()
    db.close()

    flash("Produto excluído com sucesso!", "success")
    return redirect(url_for('lista_produtos'))

# Rota para adicionar participante
# @app.route("/produtos/<int:id>/adicionar_participante", methods=['POST'])
# def adicionar_participante(id):
#     db = SessionLocal()
#     try:
#         analise = db.query(Analise).filter_by(id=id).first()
#         if not analise:
#             flash('Análise não encontrada', 'error')
#             return redirect(url_for('lista_analises'))

#         usuario_id = request.form.get('usuario_id')
#         if not usuario_id:
#             flash('Usuário não especificado', 'error')
#             return redirect(url_for('detalhes_analise', id=id))

#         # Busca apenas usuários ativos
#         usuario = db.query(Usuario).filter_by(id=usuario_id, ativo="Ativo").first()
#         if not usuario:
#             flash('Usuário inválido ou inativo', 'error')
#             return redirect(url_for('detalhes_analise', id=id))

#         if usuario in analise.participantes:
#             flash('Usuário já adicionado', 'warning')
#         else:
#             analise.participantes.append(usuario)
#             db.commit()
#             flash('Participante adicionado com sucesso', 'success')

#     except Exception as e:
#         db.rollback()
#         flash(f'Ocorreu um erro: {str(e)}', 'error')
#     finally:
#         db.close()

#     return redirect(url_for('detalhes_analise', id=id))

# @app.route("/produtos/<int:id>/remover_participante", methods=['POST'])
# def remover_participante(id):
#     db = SessionLocal()
#     try:
#         analise = db.query(Analise).filter_by(id=id).first()
#         if not analise:
#             flash('Análise não encontrada', 'error')
#             return redirect(url_for('lista_analises'))

#         usuario_id = request.form.get('usuario_id')
#         if not usuario_id:
#             flash('Usuário não especificado', 'error')
#             return redirect(url_for('detalhes_analise', id=id))

#         usuario = db.query(Usuario).filter_by(id=usuario_id).first()
#         if not usuario:
#             flash('Usuário inválido', 'error')
#             return redirect(url_for('detalhes_analise', id=id))

#         if usuario in analise.participantes:
#             analise.participantes.remove(usuario)
#             db.commit()
#             flash('Participante removido com sucesso', 'success')
#         else:
#             flash('Usuário não faz parte da análise', 'warning')

#     except Exception as e:
#         db.rollback()
#         flash(f'Ocorreu um erro: {str(e)}', 'error')
#     finally:
#         db.close()

#     return redirect(url_for('detalhes_analise', id=id))
