from flask import Flask

# Criação de uma instância do Flask
app = Flask(__name__)

# Chave secreta para criptografar a sessão
app.config['SECRET_KEY'] = 'minha_chave_secreta'

from controllers.usuario_controller import *
from controllers.aluno_controller import *
from controllers.analise_controller import *
from controllers.amostra_controller import *

#Inicia o servidor de desenvolvimento.
if __name__ == '__main__':
    app.run(debug=True)