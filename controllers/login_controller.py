from flask import flash, redirect, request
from main import app

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']
    
    if email == 'clara123@gmail.com' and senha == '123':
        return redirect('/painel_aluno.html')
    else:
        return redirect('/login.html')
        
    ANALISE_DB = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    user = cursor.fetchone()
    db.close()

    if not user:
        flash("Usuário não encontrado.", "danger")
        return redirect(url_for('home'))

    if not check_password_hash(user['senha'], senha):
        flash("Senha incorreta.", "danger")
        return redirect(url_for('home'))

    session['usuario_id'] = user['id']
    session['email'] = user['email']
    return redirect(url_for('painel'))
