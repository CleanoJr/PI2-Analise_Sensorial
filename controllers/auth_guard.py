from functools import wraps
from flask import session, redirect, url_for, flash

def login_obrigatorio(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'usuario_logado' in session:
            return f(*args, **kwargs)
        else:
            flash('Você precisa estar logado para acessar esta página.', 'danger')
            return redirect(url_for('login'))
    return wrap

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.route('/login')
@login_obrigatorio
def painel():
    return render_template('login.html')
