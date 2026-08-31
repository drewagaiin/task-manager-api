# Task Manager API

API REST sencilla construida con **FastAPI** y **SQLAlchemy**, hecha como
proyecto de aprendizaje para entender la arquitectura básica de una API:
conexión a base de datos, modelos, validación de datos, y endpoints CRUD
(crear, leer, actualizar, borrar).

## ¿Qué hace?

Permite crear usuarios y asignarles tareas (to-do list), con una relación
de "uno a muchos" entre usuario y tareas.

## Stack

- **Python 3**
- **FastAPI** — framework para construir la API
- **SQLAlchemy** — ORM para hablar con la base de datos
- **Pydantic** — validación de datos de entrada/salida
- **SQLite** — base de datos (un solo archivo, sin necesidad de instalar nada aparte)

## Estructura del proyecto

```
app/
├── main.py          # Punto de entrada, junta todo
├── database.py       # Conexión a la base de datos
├── models.py         # Tablas (User, Task) como clases de SQLAlchemy
├── schemas.py         # Qué datos son válidos para entrar/salir de la API
├── crud.py            # Lógica de creación/lectura/actualización/borrado
├── dependencies.py    # Manejo de la sesión de base de datos por request
└── routers/
    ├── users.py       # Endpoints de /users
    └── tasks.py        # Endpoints de /tasks
```

## Cómo correrlo

1. Instala las dependencias:

   ```
   pip install -r requirements.txt
   ```

2. Levanta el servidor:

   ```
   python -m uvicorn app.main:app --reload
   ```

3. Abre el navegador en `http://127.0.0.1:8000/docs` para ver la
   documentación interactiva (Swagger) y probar cada endpoint.

## Endpoints principales

| Método | Ruta                | Qué hace                          |
|--------|---------------------|------------------------------------|
| POST   | `/users/`           | Crear un usuario                   |
| GET    | `/users/`           | Listar usuarios                    |
| GET    | `/users/{id}`       | Ver un usuario (con sus tareas)    |
| POST   | `/tasks/?owner_id=X` | Crear una tarea para el usuario X |
| GET    | `/tasks/`           | Listar tareas                      |
| GET    | `/tasks/{id}`       | Ver una tarea                      |
| PATCH  | `/tasks/{id}`       | Actualizar una tarea                |
| DELETE | `/tasks/{id}`       | Borrar una tarea                    |

## Notas de aprendizaje

Este proyecto fue construido paso a paso junto con Claude, como ejercicio
para entender arquitectura de APIs REST en Python antes de pasar a otras
arquitecturas o enfoques.
