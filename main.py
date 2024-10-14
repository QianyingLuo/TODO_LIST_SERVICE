from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, g, abort
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, Tarea
import db


app = Flask(__name__)
app.secret_key = 'dev'

@app.route("/")
def index():
    if session.get("user_id"):
        return redirect(url_for("tareas"))
    return render_template("index.html")


@app.route("/registrarse", methods=["GET", "POST"])
def registrarse():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = User(username, generate_password_hash(password))

        error = None

        user_name = db.session.query(User).filter_by(username=username).first()
        if user_name == None:
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            error = f'El usuario {username} ya está registrado'

        flash(error)

    return render_template("registrarse.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        error = None
        # Validar datos
        user = db.session.query(User).filter_by(username=username).first()
        if user == None or not check_password_hash(user.password, password):
            error = 'El nombre de usuario o la contraseña no son válidos'

        # Iniciar sesión
        if error is None:
            session.clear()  # Cerrar la sesión si hay alguna que está abierta
            session['user_id'] = user.id
            return redirect(url_for("tareas"))

        flash(error)
    return render_template("login.html")


@app.before_request  # registrar la función para que se ejecute antes de cada request, para verificar si la persona ha iniciado la sesión o no
def load_logged_in_user():
    user_id = session.get('user_id')
    
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.get(User, user_id)
        if not g.user:
            print("La conexión a la base de datos ha caído.")
            abort(500)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

import functools

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.route("/tareas")
@login_required
def tareas():
    todas_las_tareas = db.session.query(Tarea).all()
    # for i in todas_las_tareas:
    #    print(i)
    return render_template("todo.html", lista_de_tareas=todas_las_tareas)  # para comunicar python con html


@app.route("/crear-tarea", methods=["POST"])
def crear():
    contenido = request.form["contenido_tarea"]
    categoria = request.form["categoria_tarea"]

    fecha_string = request.form["datepicker"]
    fecha = None

    if fecha_string:
        fecha = datetime.fromisoformat(request.form["datepicker"])

    if not all([contenido, categoria, fecha]):
        flash("Todos los campos son obligatorios", "error")

    else:
        tarea = Tarea(
            creado_por=g.user.id,
            contenido=contenido,
            categoria=categoria,
            fecha=fecha,
            hecha=False
        )  # conectar html con python

        db.session.add(tarea)
        db.session.commit()

    return redirect(url_for("tareas"))      # Esto nos redirecciona a la función home


@app.route("/eliminar-tarea/<id>")  # id es una variable
def eliminar(id):
    tarea = db.session.query(Tarea).filter_by(id=int(id))
    tarea.delete()
    db.session.commit()
    return redirect(url_for("tareas"))


@app.route("/tarea-hecha/<id>")
def hecha(id):
    tarea = db.session.query(Tarea).filter_by(id=int(id)).first()
    tarea.hecha = not (tarea.hecha)
    db.session.commit()
    return redirect(url_for("tareas"))


@app.route("/editar-tarea/<id>", methods=["POST"])
def editar(id):
    print("IDDDD", id)
    nuevo_contenido = request.form["editar_tarea"]
    nueva_categoria = request.form["nueva_categoria"]
    nueva_fecha_string = request.form["nuevo_datepicker"]

    nueva_fecha = None

    if nueva_fecha_string:
        nueva_fecha = datetime.fromisoformat(request.form["nuevo_datepicker"])

    if not all([nuevo_contenido, nueva_categoria, nueva_fecha_string]):
        flash("Todos los campos son obligatorios", "error")

    else:
        db.session.query(Tarea).filter_by(id=int(id)).update({"contenido": nuevo_contenido})
        db.session.query(Tarea).filter_by(id=int(id)).update({"categoria": nueva_categoria})
        db.session.query(Tarea).filter_by(id=int(id)).update({"fecha": nueva_fecha})
        db.session.commit()

    return redirect(url_for("tareas"))


if __name__ == "__main__":
    # En la siguiente linea estamos indicando a SQLAlchemy que cree, si no existen,
    # las tablas de todos los modelos que encuentre en models.py
    db.Base.metadata.create_all(db.engine)
    app.run(debug=True)
