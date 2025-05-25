from flask import Flask, request, render_template_string, redirect, session
from flask_mysqldb import MySQL
import bcrypt

app = Flask(__name__)
app.secret_key = 'chave_secreta'

# Configuração do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'seu_usuario'
app.config['MYSQL_PASSWORD'] = 'sua_senha'
app.config['MYSQL_DB'] = 'nome_do_banco'

mysql = MySQL(app)

# HTML Simples
login_html = '''
    <form action="{{ url_for('admin')}}" method="GET">
      <div class="mb-3">
        <input type="text" id="username" class="form-control" placeholder="Usuário" required />
      </div>
      <div class="mb-3">
        <input type="password" id="password" class="form-control" placeholder="Senha" required />
      </div>
      <button type="submit" class="btn btn-ifce w-100">Entrar</button>
    </form>
'''

@app.route('admin', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password'].encode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("SELECT senha FROM usuarios WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.checkpw(password, user[0].encode('utf-8')):
            session['usuario'] = username
            return f'Bem-vindo, {username}!'
        else:
            return 'Login inválido'

    return render_template_string(login_html)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['password'].encode('utf-8')
        hash_senha = bcrypt.hashpw(senha, bcrypt.gensalt())

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (username, senha) VALUES (%s, %s)", (username, hash_senha.decode('utf-8')))
        mysql.connection.commit()
        cur.close()

        return redirect('/login')
    return render_template_string(login_html)

if __name__ == '__main__':
    app.run(debug=True)
