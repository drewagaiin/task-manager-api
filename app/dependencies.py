"""
Aquí vive get_db: la función que le da a cada request su propia sesión
de base de datos, y se asegura de cerrarla cuando termina.

La separamos en su propio archivo (en vez de dejarla en main.py) para
evitar un problema común: si routers/tasks.py y routers/users.py
necesitan importar get_db desde main.py, y main.py a su vez importa
esos routers, se forma un "import circular" que Python no puede resolver.
Poniéndola aquí, todos importan de un mismo lugar neutral.
"""

from .database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
