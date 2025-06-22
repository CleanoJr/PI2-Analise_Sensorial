from flask import Flask, render_template, request, redirect, url_for, session, flash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'segredo123'  # Chave de sessão

# Função para proteger rotas
def login_obrigatorio(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'usuario_logado' in session:
            return f(*args, **kwargs)
        else:
            flash('Você precisa estar logado para acessar esta página.', 'danger')
            return redirect(url_for('login'))
    return wrap

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        senha = request.form['senha']
        
        # Autenticação simples (simula banco de dados)
        if usuario == 'admin' and senha == '123':
            session['usuario_logado'] = usuario
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Usuário ou senha incorretos.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html')

# Página protegida
@app.route('/admin')
@login_obrigatorio
def home():
    return render_template('login.html', usuario=session['usuario_logado'])

# Logout
@app.route('/logout')
def logout():
    session.pop('usuario_logado', None)
    flash('Logout realizado com sucesso.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
