from main import app
from flask import request, render_template, redirect, url_for, flash, session
from models.analise_model import Analise
from models.amostra_model import Amostra
from models.usuario_model import Usuario
from models.avaliacao_modal import Avaliacao
import itertools
from models.conexao import *
from sqlalchemy.orm import sessionmaker  # Importação da sessionmaker
from sqlalchemy.orm import joinedload

# Criando a sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Rota para listar todas as análises
@app.route("/analise/list", methods=['GET'])
def lista_analises():
    db = SessionLocal()
    try:
        analises = db.query(Analise).options(joinedload(Analise.responsavel)).all()
        # Força o acesso ao relacionamento para garantir que esteja carregado
        for analise in analises:
            _ = analise.responsavel
        return render_template("/analises/list_analises.html", analises=analises)
    finally:
        db.close()

# Rota para exibir formulário de cadastro
@app.route("/analise/cadastro", methods=['GET'])
def form_analise():
    db = SessionLocal()
    # Busca apenas professores ativos
    professores = db.query(Usuario).filter_by(tipo="professor", ativo="Ativo").all()
    db.close()
    return render_template("/analises/nova_analise.html", professores=professores)

# Rota para criar nova análise
@app.route("/analise/nova", methods=['POST'])
def nova_analise():
    if request.method == 'POST':
        produto = request.form['produto']
        responsavel_id = request.form['responsavel']
        grau_de_escala = request.form['grau_de_escala']
        data = request.form['data']
        status = request.form['status']
        teste = request.form['teste']
        justificativa = request.form['justificativa']


        db = SessionLocal()
        # Valida o professor selecionado
        responsavel = db.query(Usuario).filter_by(id=responsavel_id, tipo="professor", ativo="Ativo").first()
        if not responsavel:
            db.close()
            flash("Professor inválido!", "error")
            return redirect(url_for('form_analise'))

        nova_analise = Analise(
            produto=produto,
            responsavel_id=responsavel_id,
            grau_de_escala=grau_de_escala,
            data=data,
            status=status,
            teste=teste,
            justificativa=justificativa,

        )

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
    try:
        analise = db.query(Analise).options(
            joinedload(Analise.participantes),
            joinedload(Analise.responsavel)
        ).filter_by(id=id).first()
        
        if not analise:
            flash("Análise não encontrada!", "error")
            return redirect(url_for('lista_analises'))
        
        amostras = analise.amostras
        usuarios = db.query(Usuario).filter_by(ativo="Ativo").all()
        
        return render_template(
            "/analises/detalhe_analise.html",
            analise=analise,
            amostras=amostras,
            usuarios=usuarios
        )
    finally:
        db.close()

# Rota para exibir formulário de edição
@app.route("/analise/<int:id>/editar", methods=['GET'])
def form_editar_analise(id):
    db = SessionLocal()
    analise = db.query(Analise).filter_by(id=id).first()
    professores = db.query(Usuario).filter_by(tipo="professor", ativo="Ativo").all()
    if not analise:
        db.close()
        flash("Análise não encontrada!", "error")
        return redirect(url_for('lista_analises'))
    db.close()
    return render_template("/analises/edit_analise.html", analise=analise, professores=professores)

# Rota para atualizar uma análise
@app.route("/analise/<int:id>/editar", methods=['POST'])
def editar_analise(id):
    db = SessionLocal()
    analise = db.query(Analise).filter_by(id=id).first()
    if not analise:
        db.close()
        flash("Análise não encontrada!", "error")
        return redirect(url_for('lista_analises'))

    responsavel_id = request.form['responsavel']
    # Valida o professor selecionado
    responsavel = db.query(Usuario).filter_by(id=responsavel_id, tipo="professor", ativo="Ativo").first()
    if not responsavel:
        db.close()
        flash("Professor inválido!", "error")
        return redirect(url_for('form_editar_analise', id=id))

    analise.produto = request.form['produto']
    analise.responsavel_id = responsavel_id
    analise.grau_de_escala = request.form['grau_de_escala']
    analise.data = request.form['data']
    analise.status = request.form['status']
    analise.teste = request.form['teste']
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

# Rota para mostrar o dpf com a distribuicao das avaliacoes
@app.route("/analise/avaliacoes/<int:id>", methods=['GET'])
def visualizar_distribuicao_avaliacoes(id, ):
    db = SessionLocal()  
    amostras = db.query(Amostra).filter_by(analise_id=id).all()
    idsdasAmostras = [obj.id for obj in amostras]
    qtdTestadores = 120
    permutacoes = list(itertools.permutations(idsdasAmostras))
    cont = 0
    #limitar a quantidade de testadores
    while(cont < 120):
      for idx, p in enumerate(permutacoes, start=1):       
        for i in range(len(p)):
          cont = cont+1
          nova_avalicao = Avaliacao(
             numero = cont,
             status = 'criado',
             amostra_id = p[i]  
          )          
          db.add(nova_avalicao)     
         
    db.commit()
    db.close()  
    return  permutacoes
   # return redirect(url_for('detalhes_analise', id=id))