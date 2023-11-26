from flask import Flask, redirect, render_template, request, url_for, flash, abort, jsonify
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from functools import wraps
from config import config
from models.ModelUsers import ModelUsers
from models.entities.users import User

app = Flask(__name__)
app.config.from_object(config['development'])
db = MySQL(app)
login_manager_app = LoginManager(app)


@login_manager_app.user_loader
def load_user(id):
    return ModelUsers.get_by_id(db, id)


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or current_user.usertype != 1:
            abort(403)
        return func(*args, **kwargs)

    return decorated_view


@app.route("/")
def index():
    return redirect("login")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        print(
            f"Intento de inicio de sesión: Usuario - {usuario}, Contraseña - {contrasena}")

        user = User(0, usuario, contrasena, 0)
        logged_user = ModelUsers.login(db, user)

        if logged_user is not None:
            print(f"Usuario autenticado: {logged_user}")
            login_user(logged_user)
            return redirect(url_for("principal"))
        else:
            flash("Acceso rechazado. Verifica usuario y contraseña.")
            return render_template("auth/login.html")
    else:
        return render_template("auth/login.html")


@app.route("/principal")
@login_required
def principal():
    return render_template("main.html")


@app.route("/acerca")
@login_required
def acerca():
    return render_template("Acerca_de.html")


@app.route("/catalogo")
@login_required
@admin_required
def catalogo():
    return render_template("catalogo.html")


@app.route("/ticket")
@login_required
def ticket():
    return render_template("ticket.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route("/agregar_producto", methods=["POST"])
@login_required
@admin_required
def agregar_producto():
    if request.method == "POST":
        nombre = request.form['nombre']
        imagen = request.form['imagen']
        precio = request.form['precio']
        ModelUsers.agregar_producto(db, nombre, imagen, precio)

    return redirect(url_for("catalogo"))


@app.route("/editar_producto/<int:id>", methods=["POST"])
@login_required
@admin_required
def editar_producto(id):
    if request.method == "POST":
        nuevo_nombre = request.form.get("nombre")
        nueva_imagen = request.form.get("imagen")
        nuevo_precio = request.form.get("precio")
        ModelUsers.actualizar_producto(
            db, id, nuevo_nombre, nueva_imagen, nuevo_precio)
        return jsonify(success=True)
    return jsonify(success=False)


@app.route("/eliminar_producto/<int:id>", methods=["POST"])
@login_required
@admin_required
def eliminar_producto(id):
    ModelUsers.eliminar_producto(db, id)
    return redirect(url_for("catalogo"))


@app.route('/mostrar_productos')
def mostrar_productos():
    try:
        productos = ModelUsers.obtener_todos_los_productos(db)
        return render_template('catalogo.html', productos=productos)
    except Exception as ex:
        return f"Error: {ex}"

# Obtener productos como JSON


@app.route('/obtener_productos', methods=['GET'])
def obtener_productos():
    try:
        productos = ModelUsers.obtener_todos_los_productos(db)
        # Estructurar los datos como un diccionario con una clave 'productos'
        return jsonify({"productos": productos})
    except Exception as ex:
        return jsonify(error=str(ex)), 500


@app.route("/mostrar_usuarios")
@login_required
@admin_required
def mostrar_usuarios():
    try:
        usuarios = ModelUsers.obtener_todos_los_usuarios(db)

        # Excluye la contraseña al pasar los datos a la plantilla
        usuarios_data = [
            {
                'id': usuario.id,
                'username': usuario.username,
                'fullname': usuario.fullname,
                'usertype': usuario.password,
                'password': usuario.usertype
            }
            for usuario in usuarios
        ]

        return render_template('usuarios.html',  usuarios=usuarios_data)
    except Exception as ex:
        return f"Error: {ex}"


@app.route("/agregar_usuario", methods=["POST"])
@login_required
@admin_required
def agregar_usuario():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        fullname = request.form['fullname']
        usertype = request.form['usertype']
        ModelUsers.agregar_usuario(db, username, password, fullname, usertype)

    return redirect(url_for("mostrar_usuarios"))


@app.route("/editar_usuario/<int:usuario_id>", methods=["GET", "POST"])
@login_required
@admin_required
def editar_usuario(usuario_id):
    try:
        if request.method == "POST":
            username = request.form.get('username')
            password = request.form.get('password')  # Agregado
            fullname = request.form.get('fullname')
            usertype = request.form.get('usertype')

            if username is not None and password is not None and fullname is not None and usertype is not None:
                ModelUsers.actualizar_usuario(
                    db, usuario_id, username, password, fullname, usertype)
                return jsonify(success=True)

            return jsonify(success=False, error="Campos requeridos faltantes")

        # For GET requests, return the existing user information
        user = ModelUsers.obtener_usuario_por_id(db, usuario_id)
        if user:
            return render_template("edit_user.html", usuario=user)
        else:
            return jsonify(success=False, error="Usuario no encontrado")

    except Exception as ex:
        return jsonify(success=False, error=str(ex)), 500


@app.route("/eliminar_usuario/<int:id>", methods=["POST"])
@login_required
@admin_required
def eliminar_usuario(id):
    ModelUsers.eliminar_usuario(db, id)
    return redirect(url_for("mostrar_usuarios"))


@app.route("/tienda")
@login_required
def tienda():
    try:
        productos = ModelUsers.obtener_todos_los_productos(db)
        return render_template("tienda.html", productos=productos)
    except Exception as ex:
        return f"Error: {ex}"


if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(debug=True)
