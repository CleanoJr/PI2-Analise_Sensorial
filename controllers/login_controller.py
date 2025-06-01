from flask import Flask, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # Necessário para usar sessões

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'nome' not in session:
            return redirect(url_for('login'))  # Redireciona se não estiver logado
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route('/painel')
@login_required
def painel():
    nome = session['nome']
    return render_template_string('''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Painel</title>
        </head>
        <body>
            Bem vindo ao Painel, {{ nome }}.

            <p>
                <a href="{{ url_for('logout') }}">Sair</a>
            </p>
        </body>
        </html>
    ''', nome=nome)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return "Página de login (simulada)"

if __name__ == '__main__':
    app.run(debug=True)
