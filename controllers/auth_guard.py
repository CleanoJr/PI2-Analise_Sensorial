from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # importante para sessões

# Função decoradora que exige login
def login_obrigatorio(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'usuario_logado' in session:
            return f(*args, **kwargs)
        else:
            flash('Faça login para acessar esta página.', 'danger')
            return redirect(url_for('login'))
    return wrap

# Rota de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        senha = request.form['senha']

        # Autenticação simples (substitua por banco de dados real)
        if usuario == 'admin' and senha == '123':
            session['usuario_logado'] = usuario
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('painel_admin'))
        else:
            flash('Usuário ou senha incorretos.', 'danger')

    return render_template('login.html')

# Rota protegida
@app.route('/login')
@login_obrigatorio
def login():
    return render_template('painel_admin.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    flash('Você saiu com sucesso.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
