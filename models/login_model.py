from flask import Flask, request, redirect, session, render_template_string
import sqlite3  # ou use pymysql para MySQL
import hashlib

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessário para sessões

def get_db_connection():
    conn = sqlite3.connect('analise.db')  # Altere conforme seu banco
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        if not email:
            return "Preencha seu e-mail"
        elif not senha:
            return "Preencha sua senha"
        else:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Hash da senha pode ser utilizado por segurança
            # senha_hash = hashlib.sha256(senha.encode()).hexdigest()

            cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
            usuario = cursor.fetchone()
            conn.close()

            if usuario:
                session['id'] = usuario['id']
                session['nome'] = usuario['nome']
                return redirect('/painel')  # redireciona para painel
            else:
                return "Falha ao logar! E-mail ou senha incorretos"

    # Exemplo simples de formulário se o método for GET
    return render_template_string('''
        <form method="post">
            Email: <input type="text" name="email"><br>
            Senha: <input type="password" name="senha"><br>
            <input type="submit" value="Entrar">
        </form>
    ''')

@app.route('/painel')
def painel():
    if 'id' in session:
        return f"Bem-vindo, {session['nome']}!"
    else:
        return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)

    
from flask import Flask, session, redirect

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessário para usar sessões

@app.route('/logout')
def logout():
    session.clear()  # Equivalente a session_destroy() do PHP
    return redirect('/index')  # Redireciona para a página inicial (index)

@app.route('/index')
def index():
    return "Você está na página inicial."

if __name__ == '__main__':
    app.run(debug=True)
