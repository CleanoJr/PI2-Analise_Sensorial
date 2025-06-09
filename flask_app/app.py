from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from config import ANALISE_DB

app = Flask(__name__)
app.secret_key = 'chave-muito-secreta'

def get_db():
    return mysql.connector.connect(**ANALISE_DB)

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']
    
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    user = cursor.fetchone()
    db.close()

    if user and check_password_hash(user['senha'], senha):
        session['usuario_id'] = user['id']
        session['email'] = user['email']
        return redirect(url_for('painel_aluno.html'))
    return "Login inválido."

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == 'POST':
        email = request.form['email']
        senha = generate_password_hash(request.form['senha'])

        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO usuarios (email, senha) VALUES (%s, %s)", (email, senha))
        db.commit()
        db.close()
        return redirect(url_for('home'))

    return render_template('aluno_professor.html')

@app.route('/painel_aluno.html')
def painel():
    if 'usuario_id' not in session:
        return redirect(url_for('home'))
    return render_template('painel_aluno.html', email=session['email'])

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
