"""
Capa de conexión a la base de datos.

Esta es la única parte del proyecto que sabe que estamos usando SQLite.
Si mañana cambias a Postgres, MySQL, etc., en teoría solo tocas este archivo
(y la URL de conexión) — el resto del código (models, crud, routers)
no debería enterarse del cambio.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite guarda todo en un archivo local llamado tasks.db.
# check_same_thread=False es una particularidad de SQLite + FastAPI:
# SQLite por defecto solo permite usar una conexión desde el thread que
# la creó, pero FastAPI puede manejar requests en threads distintos.
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal es una "fábrica" de sesiones. Cada request a la API
# va a pedir su propia sesión (ver la función get_db más abajo, en main.py).
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base es la clase de la que heredan todos nuestros modelos (tablas).
Base = declarative_base()
