"""
Aquí definimos las "tablas" de la base de datos, pero como si fueran
clases de Python. Esto es lo que se llama un ORM (Object-Relational Mapper):
en vez de escribir SQL a mano, escribes clases, y SQLAlchemy las traduce
a tablas por debajo.
"""

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)

    # Esto NO crea una columna en la tabla. Es un "atajo" que le dice a
    # SQLAlchemy: "cuando tenga un User, déjame acceder fácilmente a
    # todas sus tareas con user.tasks". La relación real vive en la
    # columna owner_id de la tabla Task, de ahí para abajo.
    tasks = relationship("Task", back_populates="owner", cascade="all, delete-orphan")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)

    # Esta es la columna que de verdad conecta una tarea con un usuario:
    # guarda el id del usuario dueño de esta tarea.
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Y este es el atajo inverso: desde una Task, poder hacer task.owner
    # para llegar directo al User dueño, sin tener que buscarlo aparte.
    owner = relationship("User", back_populates="tasks")
