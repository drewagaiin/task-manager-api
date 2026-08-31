"""
Aquí van las funciones que realmente hablan con la base de datos:
crear, leer, actualizar, borrar (CRUD = Create, Read, Update, Delete).

La idea de tener este archivo separado de las rutas (routers/) es que
las rutas se encargan de "recibir la petición HTTP y responder", y crud.py
se encarga de "la lógica real con la base de datos". Así, si mañana
quisieras usar esta misma lógica desde otro lugar (un script, otro
endpoint), no tienes que copiar y pegar código.
"""

from sqlalchemy.orm import Session

from . import models, schemas


# ---------- Users ----------

def get_user(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[models.User]:
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)      # marca el objeto para guardarlo
    db.commit()          # lo guarda de verdad en tasks.db
    db.refresh(db_user)  # recarga db_user con el id que le asignó la BD
    return db_user


# ---------- Tasks ----------

def get_task(db: Session, task_id: int) -> models.Task | None:
    return db.query(models.Task).filter(models.Task.id == task_id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100) -> list[models.Task]:
    return db.query(models.Task).offset(skip).limit(limit).all()


def create_task(db: Session, task: schemas.TaskCreate, owner_id: int) -> models.Task:
    db_task = models.Task(**task.model_dump(), owner_id=owner_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate) -> models.Task | None:
    db_task = get_task(db, task_id)
    if db_task is None:
        return None

    # Solo actualizamos los campos que sí vinieron en la petición
    # (exclude_unset=True ignora los que quedaron en None por defecto).
    updates = task_update.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(db_task, field, value)

    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    db_task = get_task(db, task_id)
    if db_task is None:
        return False
    db.delete(db_task)
    db.commit()
    return True
