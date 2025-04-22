from main import app
from flask import render_template

@app.route("/admin", methods=['GET'])
def admin():
    return render_template("/professor/painel_professor.html")