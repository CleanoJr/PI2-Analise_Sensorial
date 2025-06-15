from flask import Flask, render_template, redirect, request, flash, send_from_directory, url_for
import json
import ast
import os
from pathlib import Path
import mysql.connector
from flask import flash, redirect, request
from models import usuario_model

from main import app
from flask import request, render_template, redirect, url_for, flash
from sqlalchemy.orm import sessionmaker  # Importação da sessionmaker


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ANALISESENSORIAL'

logado = False

@app.route('/')
def home():
    global logado
    logado = False
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    global logado
    login = request.form.get('login')
    senha = request.form.get('senha')

    analise_db = mysql.connector.connect(host='localhost', database='usuarios',user='root', password='')
    cont = 0
    if analise_db.is_connected():
        print('conectado')
        cursur = analise_db.cursor()
        cursur.execute('select * from usuario;')
        analise_db = cursur.fetchall()

        for usuario in analise_db:
            cont += 1
            usuarioLogin = str(login[1])
            usuarioSenha = str(usuario[2])

            if usuarioLogin == login and usuarioSenha == senha:
                logado = True
                return redirect('/usuarios')
            
            if cont >= len(analise_db):
                flash('USUARIO INVALIDO')
                return redirect("/")
    else:
        return redirect('/')

if __name__ in "__main__":
    app.run(debug=True)   
        