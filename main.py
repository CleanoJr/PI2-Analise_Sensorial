from flask import Flask

# Criação de uma instância do Flask
app = Flask(__name__)

from controllers.professor_controller import *

#Inicia o servidor de desenvolvimento.
if __name__ == '__main__':
    app.run()