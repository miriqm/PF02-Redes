
from flask import Flask, request, jsonify, render_template
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DATABASE = "tareas.db"


# -------------------------
# Conexión a la base de datos
# -------------------------
def conectar_db():
    conexion = sqlite3.connect(DATABASE)
    conexion.row_factory = sqlite3.Row
    return conexion


# -------------------------
# Crear tablas
# -------------------------
def crear_tablas():
    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            contraseña TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descripcion TEXT NOT NULL,
            usuario_id INTEGER REFERENCES usuarios(id)
        )
    """)

    cursor.execute("PRAGMA table_info(tareas)")
    columnas_tareas = {columna["name"] for columna in cursor.fetchall()}
    if "usuario_id" not in columnas_tareas:
        cursor.execute(
            "ALTER TABLE tareas ADD COLUMN usuario_id INTEGER REFERENCES usuarios(id)"
        )

    conexion.commit()
    conexion.close()


# -------------------------
# Registro de usuarios
# -------------------------
@app.route("/registro", methods=["POST"])
def registro():

    datos = request.get_json()

    if not datos or "usuario" not in datos or "contraseña" not in datos:
        return jsonify({
            "error": "Debe enviar usuario y contraseña"
        }), 400

    usuario = datos["usuario"]
    contraseña = datos["contraseña"]

    # Hashear la contraseña antes de guardarla
    contraseña_hash = generate_password_hash(contraseña)

    conexion = conectar_db()
    cursor = conexion.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuarios (usuario, contraseña) VALUES (?, ?)",
            (usuario, contraseña_hash)
        )

        conexion.commit()

    except sqlite3.IntegrityError:
        conexion.close()

        return jsonify({
            "error": "El usuario ya existe"
        }), 409

    conexion.close()

    return jsonify({
        "mensaje": "Usuario registrado correctamente"
    }), 201


# -------------------------
# Inicio de sesión
# -------------------------
@app.route("/login", methods=["POST"])
def login():

    datos = request.get_json()

    if not datos or "usuario" not in datos or "contraseña" not in datos:
        return jsonify({
            "error": "Debe enviar usuario y contraseña"
        }), 400

    usuario = datos["usuario"]
    contraseña = datos["contraseña"]

    conexion = conectar_db()
    cursor = conexion.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario = ?",
        (usuario,)
    )

    usuario_db = cursor.fetchone()
    conexion.close()

    if usuario_db and check_password_hash(
        usuario_db["contraseña"],
        contraseña
    ):
        return jsonify({
            "mensaje": "Inicio de sesión correcto",
            "usuario": usuario
        }), 200

    return jsonify({
        "error": "Usuario o contraseña incorrectos"
    }), 401


# -------------------------
# Gestión de tareas
# -------------------------
@app.route("/tareas", methods=["GET"])
def tareas():
    return render_template("tareas.html")


# -------------------------
# Gestión de tareas por usuario
# -------------------------
@app.route("/api/tareas", methods=["GET", "POST"])
def api_tareas():
    if request.method == "POST":
        datos = request.get_json()
        if (
            not datos
            or not isinstance(datos.get("usuario"), str)
            or not isinstance(datos.get("descripcion"), str)
            or not datos["usuario"].strip()
            or not datos["descripcion"].strip()
        ):
            return jsonify({
                "error": "Debe enviar usuario y descripción de la tarea"
            }), 400

        conexion = conectar_db()
        cursor = conexion.cursor()
        cursor.execute(
            "SELECT id FROM usuarios WHERE usuario = ?",
            (datos["usuario"],)
        )
        usuario_db = cursor.fetchone()
        if usuario_db is None:
            conexion.close()
            return jsonify({"error": "El usuario no existe"}), 404

        cursor.execute(
            "INSERT INTO tareas (descripcion, usuario_id) VALUES (?, ?)",
            (datos["descripcion"].strip(), usuario_db["id"])
        )
        conexion.commit()
        tarea_id = cursor.lastrowid
        conexion.close()

        return jsonify({
            "mensaje": "Tarea agregada correctamente",
            "id": tarea_id
        }), 201

    usuario = request.args.get("usuario", "").strip()
    if not usuario:
        return jsonify({"error": "Debe indicar el usuario"}), 400

    conexion = conectar_db()
    cursor = conexion.cursor()
    cursor.execute(
        "SELECT id FROM usuarios WHERE usuario = ?",
        (usuario,)
    )
    usuario_db = cursor.fetchone()
    if usuario_db is None:
        conexion.close()
        return jsonify({"error": "El usuario no existe"}), 404

    cursor.execute(
        "SELECT id, descripcion FROM tareas WHERE usuario_id = ? ORDER BY id",
        (usuario_db["id"],)
    )
    tareas_usuario = [
        dict(tarea) for tarea in cursor.fetchall()
    ]
    conexion.close()

    if not tareas_usuario:
        return jsonify({
            "mensaje": "No hay tareas cargadas para este usuario."
        }), 200

    return jsonify(tareas_usuario), 200


# -------------------------
# Inicio del servidor
# -------------------------
if __name__ == "__main__":

    crear_tablas()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
