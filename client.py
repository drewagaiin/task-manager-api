"""
Este es un script CLIENTE: no es parte de la API, es un programa aparte
que le HABLA a la API desde afuera, usando la librería `requests`.

Es justo lo que haría un frontend, un script de automatización, u otro
sistema que quiera integrarse con tu API — la diferencia es que aquí lo
hacemos con unas pocas líneas de Python en vez de una interfaz visual.

Requisito: tu API (app.main:app) debe estar corriendo en otra terminal,
normalmente en http://127.0.0.1:8000
"""

import requests

# La "base" de todas las URLs a las que le vamos a hablar.
BASE_URL = "http://127.0.0.1:8000"


def crear_usuario(nombre: str, email: str) -> dict:
    """Le pide a la API que cree un usuario nuevo."""
    respuesta = requests.post(
        f"{BASE_URL}/users/",
        json={"name": nombre, "email": email},  # requests convierte esto a JSON solo
    )
    respuesta.raise_for_status()  # si el status es 4xx/5xx, lanza un error aquí mismo
    return respuesta.json()  # convierte la respuesta JSON de vuelta a un dict de Python


def crear_tarea(owner_id: int, titulo: str, descripcion: str = "") -> dict:
    """Le pide a la API que cree una tarea para un usuario existente."""
    respuesta = requests.post(
        f"{BASE_URL}/tasks/",
        params={"owner_id": owner_id},  # esto va en la URL: ?owner_id=1
        json={"title": titulo, "description": descripcion},  # esto va en el body
    )
    respuesta.raise_for_status()
    return respuesta.json()


def listar_tareas() -> list[dict]:
    """Le pide a la API la lista completa de tareas."""
    respuesta = requests.get(f"{BASE_URL}/tasks/")
    respuesta.raise_for_status()
    return respuesta.json()


def completar_tarea(task_id: int) -> dict:
    """Le pide a la API que marque una tarea como completada."""
    respuesta = requests.patch(
        f"{BASE_URL}/tasks/{task_id}",
        json={"completed": True},
    )
    respuesta.raise_for_status()
    return respuesta.json()


if __name__ == "__main__":
    print("Creando usuario...")
    usuario = crear_usuario("Cliente de prueba", "cliente@example.com")
    print("Usuario creado:", usuario)

    print("\nCreando tarea para ese usuario...")
    tarea = crear_tarea(
        owner_id=usuario["id"],
        titulo="Probar el script cliente",
        descripcion="Verificar que requests le habla bien a la API",
    )
    print("Tarea creada:", tarea)

    print("\nMarcando la tarea como completada...")
    tarea_actualizada = completar_tarea(tarea["id"])
    print("Tarea actualizada:", tarea_actualizada)

    print("\nListando todas las tareas...")
    for t in listar_tareas():
        estado = "✔" if t["completed"] else "✘"
        print(f"  [{estado}] {t['title']} (id={t['id']}, owner_id={t['owner_id']})")
