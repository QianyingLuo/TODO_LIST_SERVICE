from flask import Flask, render_template, request, redirect, url_for
import db
from models import Tarea
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    todas_las_tareas = db.session.query(Tarea).all()
    #for i in todas_las_tareas:
    #    print(i)
    return render_template("index.html", lista_de_tareas = todas_las_tareas) # para comunicar python con html

@app.route("/crear-tarea", methods=["POST"])
def crear():
    fecha = datetime.fromisoformat(request.form["datepicker"])
    tarea = Tarea(
        contenido=request.form["contenido_tarea"],
        categoria=request.form["categoria_tarea"],
        fecha=fecha,
        hecha=False
    ) #conectar html con python
    db.session.add(tarea)
    db.session.commit()
    return redirect(url_for("home")) #Esto nos redirecciona a la función home

@app.route("/eliminar-tarea/<id>") # id es una variable
def eliminar(id):
    tarea = db.session.query(Tarea).filter_by(id=int(id))
    tarea.delete()
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/tarea-hecha/<id>")
def hecha(id):
    tarea = db.session.query(Tarea).filter_by(id=int(id)).first()
    tarea.hecha = not(tarea.hecha)
    db.session.commit()
    return redirect(url_for("home"))

if __name__ == "__main__":
    # En la siguiente linea estamos indicando a SQLAlchemy que cree, si no existen,
    # las tablas de todos los modelos que encuentre en models.py
    db.Base.metadata.create_all(db.engine)
    #from waitress import serve
    #serve(app, host="0.0.0.0", port=5000)
    app.run(debug=True)