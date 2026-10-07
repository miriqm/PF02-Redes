
import requests

URL_BASE = "http://127.0.0.1:5000"


# -------------------------
# Registrar usuario
# -------------------------
def registrar_usuario():

    print("\n--- REGISTRO ---")

    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")

    datos = {
        "usuario": usuario,
        "contraseña": contraseña
    }

    respuesta = requests.post(
        f"{URL_BASE}/registro",
        json=datos
    )

    print("\nRespuesta del servidor:")
    print(respuesta.json())


# -------------------------
# Iniciar sesión
# -------------------------
def login():

    print("\n--- INICIO DE SESIÓN ---")

    usuario = input("Usuario: ")
    contraseña = input("Contraseña: ")

    datos = {
        "usuario": usuario,
        "contraseña": contraseña
    }

    respuesta = requests.post(
        f"{URL_BASE}/login",
        json=datos
    )

    if respuesta.status_code == 200:

        print("\nInicio de sesión correcto.")
        return usuario

    else:

        print("\nError al iniciar sesión.")
        print(respuesta.json())
        return None


# -------------------------
# Agregar tarea
# -------------------------
def agregar_tarea(usuario):
    descripcion = input("Descripción de la tarea: ").strip()

    respuesta = requests.post(
        f"{URL_BASE}/api/tareas",
        json={
            "usuario": usuario,
            "descripcion": descripcion
        }
    )

    print(respuesta.json())


# -------------------------
# Listar tareas
# -------------------------
def listar_tareas(usuario):

    print("\n--- LISTA DE TAREAS ---")

    respuesta = requests.get(
        f"{URL_BASE}/api/tareas",
        params={"usuario": usuario}
    )

    if respuesta.status_code == 200:

        tareas = respuesta.json()

        if isinstance(tareas, dict):
            print(tareas.get("mensaje", "No hay tareas registradas."))

        else:
            for tarea in tareas:
                print(
                    f"{tarea['id']}. {tarea['descripcion']}"
                )

    else:
        print("Error al listar las tareas.")
        print(respuesta.json())


# -------------------------
# Ver HTML de /tareas
# -------------------------
def ver_html():
    respuesta = requests.get(f"{URL_BASE}/tareas")

    if respuesta.status_code == 200:
        print("\n--- HTML DE /tareas ---")
        print(respuesta.text)
    else:
        print("No se pudo acceder al HTML de /tareas.")


# -------------------------
# Menú principal
# -------------------------
def menu():
    usuario_actual = None

    while True:
        print("\n1) Registrar usuario")
        print("2) Login")
        print("3) Agregar tarea")
        print("4) Listar tareas")
        print("5) Ver HTML de /tareas")
        print("6) Salir")
        opcion = input("> ")
        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            usuario_actual = login()
        elif opcion == "3":
            if usuario_actual:
                agregar_tarea(usuario_actual)
            else:
                print("Debes iniciar sesión primero.")
        elif opcion == "4":
            if usuario_actual:
                listar_tareas(usuario_actual)
            else:
                print("Debes iniciar sesión primero.")
        elif opcion == "5":
            ver_html()
        elif opcion == "6":
            break
        else:
            print("Opción inválida.")


# -------------------------
# Inicio del cliente
# -------------------------
if __name__ == "__main__":
    menu()
