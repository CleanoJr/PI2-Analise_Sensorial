from flask import Flask, render_template, request
import mysql.connector
import hashlib

app = Flask(__name__)

# Configuração do banco de dados
 analise_db= analise_db
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'sistema_login'
} 
@app.route('/', methods=['GET', 'POST'])
def login():
    mensagem = ''
    if request.method == 'POST':
        username = request.form['username']
        senha = request.form['senha']
        senha_hash = hashlib.sha256(senha.encode()).hexdigest()

        try:
            conn = mysql.connector.connect(**analise_db
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM usuarios WHERE username = %s AND senha = %s"
            cursor.execute(query, (username, senha_hash))
            user = cursor.fetchone()

            if user:
                mensagem = "Login realizado com sucesso!"
                # Aqui você pode redirecionar, criar sessão, etc.
            else:
                mensagem = "Usuário ou senha incorretos!"

        except Exception as e:
            mensagem = f"Erro ao conectar ao banco de dados: {str(e)}"

        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    return render_template('login.html', mensagem=mensagem)

if __name__ == '__main__':
    app.run(debug=True)
