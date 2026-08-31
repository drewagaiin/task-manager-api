"""
Aquí definimos qué datos son válidos para entrar y salir de la API.

Diferencia clave con models.py:
- models.py define las tablas de la BASE DE DATOS (lo interno).
- schemas.py define la forma de los datos que la API recibe y devuelve
  (lo que ve el mundo exterior, quien sea que le hable a esta API).

Usamos Pydantic para esto, que es la librería que FastAPI usa por debajo
para validar automáticamente cada request que llega.
"""

from pydantic import BaseModel, EmailStr, ConfigDict


# ---------- Esquemas de Task ----------

class TaskBase(BaseModel):
    title: str
    description: str | None = None


class TaskCreate(TaskBase):
    """Lo que alguien nos manda para CREAR una tarea nueva."""
    pass


class TaskUpdate(BaseModel):
    """Lo que alguien nos manda para ACTUALIZAR una tarea existente.
    Todos los campos son opcionales, porque quizás solo quiere cambiar uno."""
    title: str | None = None
    description: str | None = None
    completed: bool | None = None


class TaskOut(TaskBase):
    """Lo que la API DEVUELVE cuando muestra una tarea."""
    id: int
    completed: bool
    owner_id: int

    # Esto le dice a Pydantic: "está bien leer estos datos directo desde
    # un objeto de SQLAlchemy (un modelo de la base de datos), no solo
    # desde un diccionario". Sin esto, TaskOut no podría convertir
    # automáticamente un Task de la base de datos en una respuesta JSON.
    model_config = ConfigDict(from_attributes=True)


# ---------- Esquemas de User ----------

class UserBase(BaseModel):
    name: str
    email: EmailStr


class UserCreate(UserBase):
    """Lo que alguien nos manda para CREAR un usuario nuevo."""
    pass


class UserOut(UserBase):
    """Lo que la API DEVUELVE cuando muestra un usuario.
    Nota que NO incluimos nada sensible aquí (como una contraseña,
    si tuviéramos una) — solo lo que es seguro mostrar hacia afuera."""
    id: int
    tasks: list[TaskOut] = []

    model_config = ConfigDict(from_attributes=True)
