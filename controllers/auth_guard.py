from functools import wraps
from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Chave secreta para a sessão

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session or not session['logged_in']:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/admin')
@login_required
def admin():
    return render_template('painel_admin.html')

@app.route('/login_process', methods=['POST'])
def login_process():
    #Simulação de autenticação
    username = request.form['username']
    password = request.form['password']
    if username == "user" and password == "password":
        session['logged_in'] = True
        return redirect(url_for('admin'))
    else:
         return "Credenciais inválidas"

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)