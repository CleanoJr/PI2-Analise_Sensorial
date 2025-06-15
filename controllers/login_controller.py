from flask import Flask, render_template, redirect, request


app = Flask(__name__)
app.config['SECRET_KEY'] = 'ANALISESENSORIAL'



@app.route('/')
def home():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():

    login = request.form.get('login')
    senha = request.form.get('senha')

    if login == self.login and senha == self.senha:

        return render_template("painel_admin.html")
    else:

        return redirect('/')
    
if __name__ in "__main__":
    app.run(debug=True)    