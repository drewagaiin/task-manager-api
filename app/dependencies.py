"""
Aquí viven las "dependencias" que FastAPI inyecta en las rutas:

- get_db: le da a cada request su propia sesión de base de datos, y se
  asegura de cerrarla cuando termina.
- verify_api_key: revisa que quien nos habla mande una API key válida,
  antes de dejarlo hacer nada.

La separamos en su propio archivo (en vez de dejarla en main.py) para
evitar un problema común: si routers/tasks.py y routers/users.py
necesitan importar estas funciones desde main.py, y main.py a su vez
importa esos routers, se forma un "import circular" que Python no puede
resolver. Poniéndolas aquí, todos importan de un mismo lugar neutral.
"""

import os

from fastapi import Header, HTTPException
from dotenv import load_dotenv

from .database import SessionLocal

# Esto lee el archivo .env (si existe) y carga sus variables como si
# fueran variables de entorno normales del sistema operativo.
load_dotenv()

# Leemos la API key esperada desde una variable de entorno, NUNCA
# escrita directo aquí en el código. Así, el secreto vive solo en tu
# máquina (en el archivo .env, que nunca se sube a GitHub), no en el
# código que sí es público.
API_KEY = os.getenv("API_KEY")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_api_key(x_api_key: str = Header(...)):
    """
    Dependencia que revisa el header 'X-API-Key' de la petición.

    Header(...) le dice a FastAPI: "este dato viene en un header HTTP
    llamado X-API-Key, y es obligatorio (los tres puntos significan
    'sin valor por defecto')". Si no viene, FastAPI responde solo con
    un error 422 antes incluso de llegar aquí.
    """
    if not API_KEY:
        # Si el servidor ni siquiera tiene configurada su propia key,
        # es un error de configuración nuestro, no de quien nos habla.
        raise HTTPException(status_code=500, detail="API_KEY no configurada en el servidor")

    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="API key inválida")
