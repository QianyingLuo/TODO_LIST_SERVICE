from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# El engine permite a sqlalchemy comunicarse con la base de datos en un dialecto concreto
# https:\\docs.sqlalchemy.org/en/14/core/engines.html
engine = create_engine('sqlite:///database/todolist.db',
                       connect_args={"check_same_thread": False})  # dialecto, dónde, cómo se llama la base de datos
# Advertencia: Crear el engine no conecta inmediatamente con la DB, eso lo hacemos luego

# Ahora creamos la sesión, lo que nos permite realizar transacciones (operaciones) dentro de nuestra DB
Session = sessionmaker(bind=engine)
session = Session()

# Ahora vamos al fichero models.py en los modelos (clases) donde queremos que se transformen en tablas
# le añadiremos esta variable y esto se encargara de mapear y vincular cada clase a cada tabla
Base = declarative_base()