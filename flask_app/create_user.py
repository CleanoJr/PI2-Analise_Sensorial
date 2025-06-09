from werkzeug.security import generate_password_hash
import mysql.connector
from config import ANALISE_DB

email = 'admin@email.com'
senha = generate_password_hash('123456')

db = mysql.connector.connect(**ANALISE_DB)
cursor = db.cursor()
cursor.execute("INSERT INTO usuarios (email, senha) VALUES (%s, %s)", (email, senha))
db.commit()
db.close()
print("Usuário criado com sucesso!")
