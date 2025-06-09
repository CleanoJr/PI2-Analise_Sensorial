
from flask import flash, redirect, request
from main import app

from flask import flash
from main import app
from flask import request, render_template, redirect, url_for, flash
from models.usuario_model import *
from sqlalchemy.orm import sessionmaker  # Importação da sessionmaker

# Criando a sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) 

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']
    
    if email == 'clara123@gmail.com' and senha == '123':
        return redirect('/painel_aluno.html')
    else:
        return redirect('/login.html')
        

    ANALISE_DB = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    user = cursor.fetchone()
    db.close()

    if not user:
        flash("Usuário não encontrado.", "danger")
        return redirect(url_for('login.html'))

    if not check_password_hash(user['senha'], senha):
        flash("Senha incorreta.", "danger")
        return redirect(url_for('login.html'))

    session['usuario_id'] = user['id']
    session['email'] = user['email']
    return redirect(url_for('painel_aluno'))
