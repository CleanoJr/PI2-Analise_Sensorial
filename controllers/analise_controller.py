from main import app
from flask import request, render_template, redirect, url_for, flash, session
from models.analise_model import Analise
from models.usuario_model import Usuario
from models.conexao import *
from sqlalchemy.orm import sessionmaker  # Importação da sessionmaker
from sqlalchemy.orm import joinedload

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
        justificativa = request.form['justificativa']

        nova_analise = Analise(
            nome=nome,
            responsavel=responsavel,
            data=data,
            status=status,
            tipo_avaliacao=tipo_avaliacao,
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
    
    # Carrega a análise com os participantes (usuarios) já vinculados
    analise = db.query(Analise).options(
        joinedload(Analise.participantes)  # Altere para `.usuarios` se esse for o nome no relacionamento
    ).filter_by(id=id).first()
    
    if not analise:
        db.close()
        flash("Análise não encontrada!", "error")
        return redirect(url_for('lista_analises'))
    
    # Acessa as amostras diretamente da instância
    amostras = analise.amostras
    
    # Usuário ativos para exibir no modal
    usuarios = db.query(Usuario).filter_by(ativo="Ativo").all()
    
    db.close()
    
    return render_template(
        "/analises/detalhe_analise.html",
        analise=analise,
        amostras=amostras,
        usuarios=usuarios
    )

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

# Rota para adicionar participante
@app.route("/analise/<int:id>/adicionar_participante", methods=['POST'])
def adicionar_participante(id):
    db = SessionLocal()
    try:
        analise = db.query(Analise).filter_by(id=id).first()
        if not analise:
            flash('Análise não encontrada', 'error')
            return redirect(url_for('lista_analises'))

        usuario_id = request.form.get('usuario_id')
        if not usuario_id:
            flash('Usuário não especificado', 'error')
            return redirect(url_for('detalhes_analise', id=id))

        # Busca apenas usuários ativos
        usuario = db.query(Usuario).filter_by(id=usuario_id, ativo="Ativo").first()
        if not usuario:
            flash('Usuário inválido ou inativo', 'error')
            return redirect(url_for('detalhes_analise', id=id))

        if usuario in analise.participantes:
            flash('Usuário já adicionado', 'warning')
        else:
            analise.participantes.append(usuario)
            db.commit()
            flash('Participante adicionado com sucesso', 'success')

    except Exception as e:
        db.rollback()
        flash(f'Ocorreu um erro: {str(e)}', 'error')
    finally:
        db.close()

    return redirect(url_for('detalhes_analise', id=id))

@app.route("/analise/<int:id>/remover_participante", methods=['POST'])
def remover_participante(id):
    db = SessionLocal()
    try:
        analise = db.query(Analise).filter_by(id=id).first()
        if not analise:
            flash('Análise não encontrada', 'error')
            return redirect(url_for('lista_analises'))

        usuario_id = request.form.get('usuario_id')
        if not usuario_id:
            flash('Usuário não especificado', 'error')
            return redirect(url_for('detalhes_analise', id=id))

        usuario = db.query(Usuario).filter_by(id=usuario_id).first()
        if not usuario:
            flash('Usuário inválido', 'error')
            return redirect(url_for('detalhes_analise', id=id))

        if usuario in analise.participantes:
            analise.participantes.remove(usuario)
            db.commit()
            flash('Participante removido com sucesso', 'success')
        else:
            flash('Usuário não faz parte da análise', 'warning')

    except Exception as e:
        db.rollback()
        flash(f'Ocorreu um erro: {str(e)}', 'error')
    finally:
        db.close()

    return redirect(url_for('detalhes_analise', id=id))