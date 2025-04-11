from main import app
from flask import render_template

@app.route("/professor", methods=['GET'])
def professor():
    return render_template("/professor/painel_professor.html")