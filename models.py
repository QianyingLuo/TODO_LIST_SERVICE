from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, String, DateTime, Text, ForeignKey
import db

class User(db.Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String(20), unique = True, nullable=False)
    password = Column(Text, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


class Tarea(db.Base):
    __tablename__ = "tarea"
    __table_args__ = {'sqlite_autoincrement': True}

    id = Column(Integer, primary_key=True)
    creado_por = Column(Integer, ForeignKey('user.id'), nullable=False)
    contenido = Column(String(200), nullable=False)
    categoria = Column(String(50), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    hecha = Column(Boolean)

    def __init__(self, creado_por, contenido, categoria, fecha, hecha):
        self.creado_por = creado_por
        self.contenido = contenido
        self.categoria = categoria
        self.fecha = fecha
        self.hecha = hecha
        print("Tarea creada con éxito")

    def __str__(self):
        return "Tarea {} (creado por: {})".format(self.contenido, self.creado_por)
