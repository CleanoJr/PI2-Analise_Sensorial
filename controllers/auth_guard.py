from main import app
from models.usuario_model import *
from models.conexao import *
from sqlalchemy.orm import sessionmaker  # Importação da sessionmaker
from functools import wraps
from flask import session, redirect, url_for, flash

# Criando a sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.route('/painel_admin')
@login_obrigatorio
def painel_admin():
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    return redirect(url_for('login'))

