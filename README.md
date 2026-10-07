# PFO 2 - Sistema de Gestión de Tareas

## Descripción

Este proyecto implementa un sistema básico de gestión de tareas utilizando una API REST desarrollada con Flask y una base de datos SQLite.

El sistema permite registrar usuarios, iniciar sesión y acceder al endpoint de tareas.

Las contraseñas se almacenan utilizando hash y nunca se guardan en texto plano.

Proyecto realizado como trabajo práctico de Programación sobre Redes.

## Tecnologías utilizadas

* Python
* Flask
* SQLite
* Werkzeug

## Estructura del proyecto

```text
PFO2/
├── server.py
├── client.py
├── templates/
│   └── tareas.html
├── tareas.db
└── README.md
```

La base de datos `tareas.db` se crea automáticamente al ejecutar el servidor.

## Instalación

Clonar el repositorio:

```bash
git clone URL_DEL_REPOSITORIO
```

Ingresar a la carpeta:

```bash
cd PFO2
```

Instalar las dependencias:

```bash
pip install flask werkzeug
```

## Ejecutar el servidor

Ejecutar:

```bash
python server.py
```

El servidor estará disponible en:

```text
http://127.0.0.1:5000
```

## Endpoints

### POST /registro

Permite registrar un nuevo usuario.

URL:

```text
http://127.0.0.1:5000/registro
```

Body JSON:

```json
{
    "usuario": "carlos",
    "contraseña": "1234"
}
```

Respuesta esperada:

```json
{
    "mensaje": "Usuario registrado correctamente"
}
```

### POST /login

Permite verificar las credenciales de un usuario registrado.

URL:

```text
http://127.0.0.1:5000/login
```

Body JSON:

```json
{
    "usuario": "carlos",
    "contraseña": "1234"
}
```

Respuesta esperada:

```json
{
    "mensaje": "Inicio de sesión correcto",
    "usuario": "carlos"
}
```

### GET /tareas

Muestra una página HTML de bienvenida.

URL:

```text
http://127.0.0.1:5000/tareas
```

Al acceder se muestra:

```text
Bienvenido al Sistema de Gestión de Tareas
```

### GET /api/tareas?usuario=carlos

Devuelve las tareas del usuario indicado en formato JSON. Si todavía no tiene
tareas, responde `200 OK` con este mensaje:

```json
{
    "mensaje": "No hay tareas cargadas para este usuario."
}
```

El cliente debe iniciar sesión antes de listar tareas.

### POST /api/tareas

Agrega una tarea al usuario indicado. Enviar un body JSON:

```json
{
    "usuario": "carlos",
    "descripcion": "Terminar el trabajo práctico"
}
```

Las tareas se guardan asociadas al usuario que las creó. La tabla existente se
actualiza automáticamente al iniciar el servidor.

## Seguridad

Las contraseñas no se almacenan en texto plano.

Para protegerlas se utiliza `generate_password_hash()` de Werkzeug.

Para comprobar una contraseña durante el login se utiliza:

```python
check_password_hash()
```

## Base de datos

El proyecto utiliza SQLite.

La base de datos contiene una tabla `usuarios` con:

* `id`
* `usuario`
* `contraseña`

La contraseña almacenada corresponde al hash generado y no a la contraseña original.

También se crea una tabla `tareas` para almacenar las tareas del sistema.

## Pruebas

Las pruebas pueden realizarse desde la consola del cliente o enviando peticiones
con Bruno. Antes de probar, inicia el servidor desde la carpeta `PFO2`:

```bash
python3 server.py
```

Deja esa consola abierta. Para probar desde el cliente, abre una segunda consola
en la misma carpeta y ejecuta:

```bash
python3 client.py
```

En el menú del cliente, prueba estas opciones en orden:

1. **Registrar usuario**: registra un usuario nuevo.
2. **Login**: inicia sesión con ese usuario.
3. **Agregar tarea**: escribe la descripción de una tarea.
4. **Listar tareas**: comprueba que aparezca la tarea agregada.
5. **Ver HTML de /tareas**: comprueba que se muestre la página HTML.
6. **Salir**: cierra el cliente.

También puedes probar la API desde Bruno. Crea las siguientes solicitudes con
la URL base `http://127.0.0.1:5000` y selecciona **Body → JSON** cuando se
indique:

| Prueba | Método y URL | Body JSON | Resultado esperado |
|---|---|---|---|
| Registrar usuario | `POST /registro` | `{"usuario":"carlos","contraseña":"1234"}` | `201 Created` y mensaje de registro correcto. |
| Iniciar sesión | `POST /login` | `{"usuario":"carlos","contraseña":"1234"}` | `200 OK` y mensaje de inicio de sesión correcto. |
| Probar credenciales incorrectas | `POST /login` | `{"usuario":"carlos","contraseña":"incorrecta"}` | `401 Unauthorized`. |
| Agregar tarea | `POST /api/tareas` | `{"usuario":"carlos","descripcion":"Terminar el trabajo práctico"}` | `201 Created` y el identificador de la tarea. |
| Listar tareas del usuario | `GET /api/tareas?usuario=carlos` | Sin body | `200 OK`, las tareas de Carlos o un mensaje si todavía no tiene. |
| Ver la página HTML | `GET /tareas` | Sin body | `200 OK` y la página HTML de bienvenida. |

Para comprobar que las tareas son individuales, registra otro usuario y consulta
`GET /api/tareas?usuario=otro_usuario`; si aún no tiene tareas, la respuesta
incluye el mensaje de que no hay tareas cargadas para ese usuario. Repetir el
registro de un usuario existente debe devolver `409 Conflict`.

## Respuestas conceptuales

### ¿Por qué hashear contraseñas?

Las contraseñas se deben hashear para evitar almacenarlas en texto plano. De esta manera, si alguien obtiene acceso a la base de datos, no puede ver directamente las contraseñas originales.

### ¿Qué ventajas tiene utilizar SQLite?

SQLite es una base de datos sencilla y liviana que no necesita un servidor independiente. Los datos se almacenan en un archivo local, lo que facilita su instalación y utilización en proyectos pequeños. Además, permite utilizar SQL y mantener los datos almacenados aunque el servidor se cierre.
