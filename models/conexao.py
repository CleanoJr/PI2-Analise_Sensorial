from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base


# URL de conexão com o banco de dados MySQL no XAMPP
DATABASE_URL = "mysql+pymysql://root:@localhost/analise_db"


# Conexão com o banco de dados MySQL usando SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)


# Classe base para os modelos
Base = declarative_base()

import mysql.connector
from mysql.connector import Error

usuario = 'root'
senha = ''
database = 'login'
host = 'localhost'

#Atualização (Jarléia)
try:
    conexao = mysql.connector.connect(
        host=host,
        user=usuario,
        password=senha,
        database=database
    )

    if conexao.is_connected():
        print("Conexão bem-sucedida ao banco de dados")

except Error as e:
    print(f"Falha ao conectar ao banco de dados: {e}")

finally:
    if 'conexao' in locals() and conexao.is_connected():
        conexao.close()
