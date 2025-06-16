from flask import request, render_template, redirect, url_for, flash
import sqlite3
import bcrypt
from main import app
from models.usuario_model import *
from models.conexao import *
from datetime import datetime  # Para converter a data corretamente
from sqlalchemy.orm import sessionmaker  # Importação da sessionmaker
import re

app = Flask(__name__)
app.secret_key = 'segredo_super_secreto'  # Use algo mais seguro em produção

# Função para conectar ao banco
def get_db_connection():
    conn = sqlite3.connect('analise.db')
    conn.row_factory = sqlite3.Row
    return conn

# Cria tabela (executar uma vez ou use outro script separado)
def criar_tabela():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_usuario TEXT NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

criar_tabela()

# Rota de login
@app.route('/', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        login_usuario = request.form['login_usuario']
        senha = request.form['senha']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM logins WHERE login_usuario = ?', (login_usuario,)).fetchone()
        conn.close()

        if user and bcrypt.checkpw(senha.encode('utf-8'), user['senha_hash']):
            session['login'] = login_usuario
            return redirect(url_for('home'))
        else:
            erro = 'Login ou senha incorretos.'

    return render_template('login.html', erro=erro)

# Página inicial (após login)
@app.route('/home')
def home():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('painel_aluno.html', nome_login=session['login'])

# Rota para logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
