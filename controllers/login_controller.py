
from flask import flash, redirect, request
from models import usuario_model

from main import app
from flask import request, render_template, redirect, url_for, flash
from sqlalchemy.orm import sessionmaker  # Importação da sessionmaker

# Criando a sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

@app.route('/login', methods=['GET', 'POST'])
def login():
    db = SessionLocal() 
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']

        user = db.session.query(usuario_model).filter_by(email=email, senha=senha).first()
        if not user:
            return 'Email ou senha incorretos.'
        