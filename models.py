from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, String, DateTime

import db

class Tarea(db.Base):

    __tablename__ = "tarea"
    __table_args__ = {'sqlite_autoincrement': True} # quiero que haya una columna actúe como identificador que autoincremente
    id = Column(Integer, primary_key=True)
    contenido = Column(String(200), nullable=False)
    categoria = Column(String(50), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    hecha = Column(Boolean)

    def __init__(self, contenido, categoria, fecha, hecha):
        self.contenido = contenido
        self.categoria = categoria
        self.fecha = fecha
        self.hecha = hecha
        print("Tarea creada con éxito")

    def __str__(self):
        return "Tarea {}: {} {} Fecha límite: {} ({})".format(self.id, self.contenido, self.categoria, self.fecha, self.hecha)