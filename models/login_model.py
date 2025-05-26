from flask import Flask, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'

# Configuração do banco (exemplo SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
db = SQLAlchemy(app)

# Modelo de Usuário
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)  # senha hashed

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = Usuario.query.filter_by(username=username).first()

    if user and check_password_hash(user.senha, password):
        session['usuario'] = username  # Guarda usuário na sessão
        return redirect(url_for('admin'))
    else:
        return "Senha incorreta."

@app.route('/admin')
def admin():
    if 'usuario' not in session:
        return redirect(url_for('login_page'))  # redireciona se não logado
    return f"Bem-vindo à área administrativa, {session['usuario']}!"

@app.route('/login')
def login_page():
    # Aqui você poderia renderizar a página de login
    return '''
    <form method="POST" action="/login">
      Usuário: <input type="text" name="username"><br>
      Senha: <input type="password" name="password"><br>
      <input type="submit" value="Login">
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)