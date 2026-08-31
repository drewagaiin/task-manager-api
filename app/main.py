"""
Punto de entrada de la aplicación. Aquí se junta todo lo que armamos:
database.py, models.py, schemas.py, crud.py y los routers.
"""

from fastapi import FastAPI

from . import models
from .database import engine
from .routers import tasks, users

# Esto crea las tablas de verdad en tasks.db, a partir de las clases
# que definimos en models.py, SI todavía no existen. Si ya existen,
# no hace nada (no borra datos).
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Task Manager API")

# Aquí "conectamos" los routers que armamos por separado.
# Todas las rutas de tasks.py van a vivir bajo /tasks,
# y todas las de users.py bajo /users.
app.include_router(users.router)
app.include_router(tasks.router)


@app.get("/")
def root():
    return {"message": "Task Manager API funcionando. Visita /docs para probarla."}
