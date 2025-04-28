from main import app
from flask import render_template

@app.route("/aluno", methods=['GET'])
def aluno():
    return render_template("/aluno/painel_aluno.html")

@app.route("/aluno/dashboard", methods=['GET'])
def aluno_dashboard():
    return render_template("/usuario_aluno/dashboard.html")

@app.route("/aluno/analise", methods=['GET'])
def aluno_analise():
    return render_template("/usuario_aluno/analise.html")

@app.route("/teste", methods=['GET'])
def teste():
    return render_template("/usuario_aluno/dashboard.html")