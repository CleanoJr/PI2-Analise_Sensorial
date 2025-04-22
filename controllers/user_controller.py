from main import app
from flask import render_template

@app.route("/login", methods=['GET'])
def login():
    return render_template("/login.html")