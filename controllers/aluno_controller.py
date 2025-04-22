from main import app
from flask import render_template

@app.route("/aluno", methods=['GET'])
def aluno():
    return render_template("/aluno/painel_aluno.html")