from main import app
from models.usuario_model import *
from models.conexao import *
from datetime import datetime  # Para converter a data corretamente
from sqlalchemy.orm import sessionmaker  # Importação da sessionmaker
import re
from flask import Flask, render_template, request, flash, redirect
import os

app = Flask(__name__)
app.config['SECRET_KEY']= "PALAVRA-SECRETA"
@app.route("/")
def home():
    return render_template("html/login.html")

@app.route("/login", methods=['POST'])
def login():
    login = request.form.get('login')
    senha = request.form.get('senha')
    with open('usuarios_controller') as usuarios:
        lista = load(usuarios)
        cont = 0
        for c in lista:
            cont+=1
            if usuario == c['login'] and senha == c['senha']:
                return render_template("/painel_aluno.html", loginUsuario=c['login'])
            if cont >= len(lista):
                flash('login invalido')
                return redirect("/")



if __name__ in '__main__':
    app.run(debug=True)