import os
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
from werkzeug.utils import secure_filename


# Importamos modelos y formularios
from models import db, Producto, Usuario
from forms import ProductoForm, RegisterForm, LoginForm
from inventory import Inventario

# Configuración de la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key'  # En producción usar variable de entorno

# Modificación aplicada: usamos PyMySQL como conector
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://proyecto_web:@localhost/mi_proyecto_flask'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#Modificación aplicada: carpeta para subir imágenes
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'uploads')

# Inicializamos la base de datos
db.init_app(app)

# Inicializamos Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirige a login si no está autenticado

# Cargador de usuario para Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Inyectamos la fecha actual en los templates
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}

# Creamos las tablas y cargamos el inventario en memoria
with app.app_context():
    db.create_all()
    inventario = Inventario.cargar_desde_bd()

# Ruta para probar conexión a la base de datos
@app.route('/test_db')
def test_db():
    try:
        conn = db.engine.connect()
        tables = conn.execute("SHOW TABLES").fetchall()
        conn.close()
        return str(tables)
    except Exception as e:
        return f"Error de conexión: {e}"

# Página principal
@app.route('/')
def index():
    return render_template('index.html', title='Inicio')

# Página "Sobre Nosotros"
@app.route('/about/')
def about():
    return render_template('about.html', title='Acerca de')

# Registro de usuario
@app.route('/registrer', methods=['GET', 'POST'])
def registrer():
    form = RegisterForm()
    modo = 'crear'
    if form.validate_on_submit():
        if Usuario.query.filter_by(email=form.email.data).first():
            flash('Ya existe un usuario con ese correo.', 'warning')
            return render_template('login/registrer.html', title='Regístrate', form=form, modo=modo)

        nuevo_usuario = Usuario(
            nombre=form.nombre.data,
            apellido=form.apellido.data,
            email=form.email.data,
            telefono=form.telefono.data,
            pais=form.pais.data,
            ciudad=form.ciudad.data,
            codigo_postal=form.codigo_postal.data,
            password=form.password.data  # ⚠️ En producción, usar hash
        )
        db.session.add(nuevo_usuario)
        db.session.commit()
        flash('Usted se ha registrado correctamente.', 'success')
        return redirect(url_for('login'))
    return render_template('login/registrer.html', title='Regístrate', form=form, modo=modo)

# Inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    modo = 'Iniciar sesión'
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and usuario.password == form.password.data:  # ⚠️ Comparación directa, usar hash en producción
            login_user(usuario)
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('index'))
        else:
            flash('Correo electrónico o contraseña incorrectos.', 'danger')
    return render_template('login/login.html', title='Iniciar sesión', form=form, modo=modo)

# Cierre de sesión
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente.', 'info')
    return redirect(url_for('index'))

#### Rutas para gestión de productos ####

# Listado de productos (requiere login)
@app.route('/productos')
@login_required
def listar_productos():
    q = request.args.get('q', '').strip()
    if q:
        productos = Producto.query.filter(Producto.nombre.like(f"%{q}%")).all()
    else:
        productos = Producto.query.all()
    return render_template('products/list.html', title='Productos', productos=productos, q=q)


# Crear nuevo producto (requiere login)
@app.route('/productos/nuevo', methods=['GET', 'POST'])
@login_required
def crear_producto():
    form = ProductoForm()
    mensaje_imagen = None

    if form.validate_on_submit():
        filename = None

        if form.imagen.data and form.imagen.data.filename != '':
            filename = secure_filename(form.imagen.data.filename)
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            ruta_completa = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            try:
                form.imagen.data.save(ruta_completa)
                mensaje_imagen = f"✅ Imagen guardada correctamente en: {ruta_completa}"
            except Exception as e:
                mensaje_imagen = f"⚠️ Error al guardar la imagen: {e}"
                filename = None

        nuevo = Producto(
            nombre=form.nombre.data,
            imagen=filename,
            descripcion=form.descripcion.data,
            categoria=form.categoria.data,
            subcategoria=form.subcategoria.data,
            talla=form.talla.data,
            color=form.color.data,
            material=form.material.data,
            cantidad=form.cantidad.data,
            precio=form.precio.data
        )

        db.session.add(nuevo)
        db.session.commit()

        flash('Producto agregado correctamente.', 'success')
        return render_template('products/form.html', title='Nuevo producto', form=form, modo='crear', mensaje_imagen=mensaje_imagen)

    return render_template('products/form.html', title='Nuevo producto', form=form, modo='crear')




# Editar producto (requiere login)
@app.route('/productos/<int:pid>/editar', methods=['GET', 'POST'])
@login_required
def editar_producto(pid):
    producto = Producto.query.get_or_404(pid)
    form = ProductoForm(obj=producto)
    if form.validate_on_submit():
        form.populate_obj(producto)
        db.session.commit()
        flash('Producto actualizado.', 'success')
        return redirect(url_for('listar_productos'))
    return render_template('products/form.html', title='Editar producto', form=form, modo='editar')

# Eliminar producto (requiere login)
@app.route('/productos/<int:pid>/eliminar', methods=['POST'])
@login_required
def eliminar_producto(pid):
    ok = inventario.eliminar(pid)
    flash('Producto eliminado.' if ok else 'Producto no encontrado.', 'info' if ok else 'warning')
    return redirect(url_for('listar_productos'))

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
