from flask import Flask, render_template, request, redirect, url_for
from models.avaliador_model import *
from models.conexao import *
app = Flask(__name__)

# Rota para exibir o termo
@app.route('/')
def termo_consentimento():
    return render_template('termo.html')  # arquivo HTML com o termo

# Rota para exibir o formulário sensorial
@app.route('/avaliacao')
def avaliacao_sensorial():
    return render_template('ficha.html')  # arquivo HTML com a ficha

# Rota para receber os dados do formulário via POST
@app.route('/avaliacao', methods=['POST'])

@app.route('/avaliacao', methods=['POST'])
def enviar_avaliacao():
    nome = request.form.get('nome')
    email = request.form.get('email')
    genero = request.form.get('genero')
    faixa_etaria = request.form.get('faixa_etaria')

    avaliador = Avaliador(
        nome=nome,
        email=email,
        genero=genero,
        faixa_etaria=faixa_etaria
    )

   
    

    return "Obrigado por sua participação!"

if __name__ == '__main__':
    app.run(debug=True)