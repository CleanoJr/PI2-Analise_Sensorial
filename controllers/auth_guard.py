from flask import Flask, render_template_string, request, session, redirect
app = Flask(__name__)
app.secret_key = 'segredo'

@app.route('/', methods=['GET', 'POST'])
def login(): return render_template_string(T, erro='Login/Senha inválidos' if request.method=='POST' and (request.form['u']!='admin' or request.form['s']!='123') else None) if request.method=='GET' or (request.form['u']=='admin' and request.form['s']=='123' and not session.setdefault('u','admin')) else redirect('/painel')

@app.route('/painel') 
def painel(): return render_template_string('<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"><div class="container mt-5"><h1>Bem-vindo, {{session["u"]}}</h1><a href="/sair" class="btn btn-danger mt-3">Sair</a></div>') if 'u' in session else redirect('/')

@app.route('/sair')
def sair(): session.clear(); return redirect('/')

T = '''<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<div class="container mt-5"><h2>Login</h2>
<form method="POST">
  <input name="l" class="form-control mb-2" placeholder="Login">
  <input name="s" type="password" class="form-control mb-2" placeholder="Senha">
  <button class="btn btn-primary">Entrar</button>
  {% if erro %}<div class="alert alert-danger mt-2">{{erro}}</div>{% endif %}
</form></div>'''

app.run(debug=True)

