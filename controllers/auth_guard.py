from main import app
from flask import request, render_template, redirect, url_for, flash
from models.usuario_model import *
from models.conexao import *
from datetime import datetime  # Para converter a data corretamente
from sqlalchemy.orm import sessionmaker  # Importação da sessionmaker


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

