from main import app
from flask import request, render_template, redirect, url_for, flash
from models.usuario_model import *
from models.conexao import *
from datetime import datetime  # Para converter a data corretamente
from sqlalchemy.orm import sessionmaker  # Importação da sessionmaker
import re

# Criando a sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.route("/", methods=['GET'])
def login():
    return render_template("/login.html")

@app.route("/admin", methods=['GET'])
def admin():
    return render_template("/professor/painel_admin.html")

# Rota para exibir o Login
@app.route("/cadastro/inserir", methods=['GET'])
def cad_inserir():
    return render_template("/cadastro/aluno_professor.html")

# Rota para processar o Login
@app.route("/cadastro/inserir/create", methods=['POST'])
def create():
    if request.method == 'POST':
        # Captura os dados enviados pelo Login
        login = request.form['login']
        senha = request.form['senha']

     # Cria um novo login
    new_login = Login(
            login=login,
            senha=senha,
            ativo='Ativo'  # Definindo o status como ativo por padrão
            )

        # Cria uma nova sessão para o banco de dados
    db = SessionLocal()

        # Adiciona o novo cadastro ao banco de dados
    db.add(new_login)
    db.commit()

        # Redireciona para a página de lista de cadastros
    flash("Login cadastrado com sucesso!", "success")
    return redirect(url_for('lista'))

# Rota para exibir a lista de cadastros
@app.route("/cadastro/inserir/list")
def lista():
    # Cria uma nova sessão para o banco de dados
    db = SessionLocal()

    # Consulta todos os cadastros no banco de dados
    cadastros = db.query(login).all()

    # Renderiza o template com a lista de cadastros
    return render_template("cadastro/list_login.html", cadastros=cadastros)

# Rota para processar a atualização
@app.route("/cadastro/inserir/update/<int:id>", methods=["POST"])
def update(id):
    db = SessionLocal()
    cadastro = db.query(Login).filter(Login.id == id).first()

    if cadastro:
        cadastro.login = request.form['login']
        cadastro.senha = request.form['senha']
        cadastro.ativo = request.form['ativo']  # Atualizando o status de Ativo/Inativo

        db.commit()
    db.close()

    flash("Login atualizado com sucesso!", "success")
    return redirect(url_for('lista'))

# Rota para excluir um cadastro
@app.route("/cadastro/excluir/<int:id>", methods=["GET"])
def excluir(id):
    # Cria uma nova sessão para o banco de dados
    db = SessionLocal()

    # Encontra o cadastro que corresponde ao ID
    Login = db.query(Login).filter(Login.id == id).first()

    if login:
        # Exclui o cadastro encontrado
        db.delete(login)
        db.commit()

    db.close()

    # Redireciona para a página de lista de cadastros após a exclusão
    flash("Login excluído com sucesso!", "success")
    return redirect(url_for('lista'))