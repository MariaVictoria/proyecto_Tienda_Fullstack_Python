from flask import Flask, render_template, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, login_required, logout_user, LoginManager, current_user
import time

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datos.db'
db = SQLAlchemy(app)
login_manager = LoginManager(app)

class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(100), unique=True)
    contrasena = db.Column(db.String(100))

class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    usuario = db.relationship('Usuario', backref=db.backref('registros', lazy=True))
    tiempo = db.Column(db.Integer)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

@app.route('/')
def inicio():
    return render_template('inicio.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        nombre_usuario = request.form['nombre_usuario']
        contrasena = request.form['contrasena']
        usuario = Usuario.query.filter_by(nombre_usuario=nombre_usuario).first()
        if usuario and usuario.contrasena == contrasena:
            login_user(usuario)
            return redirect(url_for('cronometro'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('inicio'))

@app.route('/cronometro')
@login_required
def cronometro():
    registros = Registro.query.filter_by(usuario=current_user).all()
    return render_template('cronometro.html', registros=registros)

@app.route('/tiempo')
@login_required
def obtener_tiempo():
    tiempo_transcurrido = int(time.time())  # Convertir el tiempo actual en un entero
    registro = Registro(usuario=current_user, tiempo=tiempo_transcurrido)
    db.session.add(registro)
    db.session.commit()
    return str(tiempo_transcurrido)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
