from flask import Flask, render_template_string, request, redirect, url_for
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['u'] == 'admin' and request.form['s'] == '123':
            return redirect(url_for('login_ok'))
        else:
            erro = 'Usuário ou senha incorretos.'
            return render_template_string(T, erro=erro)
    return render_template_string(T)

@app.route('/login_ok')
def login_ok():
    return render_template_string('<div class="container mt-5"><h2>Login efetuado com sucesso!</h2></div>')

T = '''<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<div class="container mt-5"><h2>Login</h2>
<form method="POST">
  <input name="u" class="form-control mb-2" placeholder="Usuário" required>
  <input name="s" type="password" class="form-control mb-2" placeholder="Senha" required>
  <button class="btn btn-primary">Entrar</button>
</form>
{% if erro %}<div class="alert alert-danger mt-2">{{erro}}</div>{% endif %}
</div>'''

app.run(debug=True)
