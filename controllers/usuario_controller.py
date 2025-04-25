from main import app
from flask import request, render_template, redirect, url_for, flash
from models.usuario_model import *
from models.conexao import *
from datetime import datetime  # Para converter a data corretamente
from sqlalchemy.orm import sessionmaker  # Importação da sessionmaker

# Criando a sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.route("/login", methods=['GET'])
def login():
    return render_template("/login.html")

@app.route("/admin", methods=['GET'])
def admin():
    return render_template("/professor/painel_admin.html")

# Rota para exibir o formulário
@app.route("/cadastro/inserir", methods=['GET'])
def cad_inserir():
    return render_template("/cadastro/aluno_professor.html")

# Rota para processar o formulário
@app.route("/cadastro/create", methods=['POST'])
def create():
    if request.method == 'POST':
        # Captura os dados enviados pelo formulário
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        data_str = request.form['data_nascimento']  # Data como string
        login = request.form['login']
        senha = request.form['senha']
        tipo = request.form['tipo']

        # Convertendo a data do formato string para o tipo Date
        data_nascimento = datetime.strptime(data_str, '%Y-%m-%d').date()

        # Cria um novo cadastro
        new_usuario = Usuario(
            nome=nome,
            email=email,
            telefone=telefone,
            login=login,
            senha=senha,
            tipo=tipo,
            data_nascimento=data_nascimento,
            ativo=request.form['ativo'] if request.form['ativo'] else "Inativo"  # Se não marcado, é "Inativo"
            )

        # Cria uma nova sessão para o banco de dados
        db = SessionLocal()

        # Adiciona o novo cadastro ao banco de dados
        db.add(new_usuario)
        db.commit()

        # Redireciona para a página de lista de cadastros
        flash("Usuario cadastrado com sucesso!", "success")
        return redirect(url_for('lista'))

# Rota para exibir a lista de cadastros
@app.route("/list")
def lista():
    # Cria uma nova sessão para o banco de dados
    db = SessionLocal()
    
    # Consulta todos os cadastros no banco de dados
    cadastros = db.query(Usuario).all()
    
    # Renderiza o template com a lista de cadastros
    return render_template("/usuario/list_usuario.html", cadastros=cadastros)

# Rota para exibir o formulário de edição
@app.route("/cadastro/editar/<int:id>", methods=["GET"])
def editar(id):
    db = SessionLocal()
    cadastro = db.query(Usuario).filter(Usuario.id == id).first()
    db.close()
    return render_template("usuario/edit_usuario.html", cadastro=cadastro)

# Rota para processar a atualização
@app.route("/cadastro/update/<int:id>", methods=["POST"])
def update(id):
    db = SessionLocal()
    cadastro = db.query(Usuario).filter(Usuario.id == id).first()

    if cadastro:
        cadastro.nome = request.form['nome']
        cadastro.email = request.form['email']
        cadastro.telefone = request.form['telefone']
        cadastro.data_nascimento = datetime.strptime(request.form['data_nascimento'], '%Y-%m-%d').date()
        cadastro.login = request.form['login']
        cadastro.senha = request.form['senha']
        cadastro.tipo = request.form['tipo']
        cadastro.ativo = request.form['ativo']  # Atualizando o status de Ativo/Inativo

        db.commit()
    db.close()

    flash("Usuario atualizado com sucesso!", "success")
    return redirect(url_for('lista'))