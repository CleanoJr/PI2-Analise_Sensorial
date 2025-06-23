from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
from sqlalchemy.orm import sessionmaker  # Importação da sessionmaker

# Criando a sessão para interagir com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
app = Flask(__name__)
app.secret_key = 'segredo'

def login_obrigatorio(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'usuario' in session:
            return f(*args, **kwargs)
        flash('Faça login primeiro.', 'danger')
        return redirect(url_for('login'))
    return wrap


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and request.form['senha'] == '123':
        session['login'] = request.form['login']
        return redirect(url_for('painel_admin'))
    flash('Login inválido.', 'danger')
    return render_template('login.html')

@app.route('/admin')
@login_obrigatorio
def painel():
    return render_template('painel_admin.html', login=session['login'])

@app.route('/logout')
def logout():
    session.pop('login', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
