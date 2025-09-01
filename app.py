from flask import Flask, render_template, redirect, url_for, flash, request
from datetime import datetime
from models import db, Producto
from forms import ProductoForm
from inventory import Inventario

# Crear la instancia principal de la aplicación Flask
app = Flask(__name__)

# Configuración de la base de datos SQLite y otras opciones
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key'  # En producción, usar variable de entorno

# Inicializar la extensión SQLAlchemy con la app
db.init_app(app)

# Inyectar la función 'now' en los templates para mostrar el año actual
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow}

# Crear las tablas en la base de datos y cargar el inventario en memoria
with app.app_context():
    db.create_all()
    inventario = Inventario.cargar_desde_bd()  # Cache en memoria con diccionario y set

# --- Rutas principales ---
@app.route('/')
def index():
    # Página de inicio
    return render_template('index.html', title='Inicio')

@app.route('/usuario/<nombre>')
def usuario(nombre):
    # Saludo personalizado al usuario
    return f'Bienvenido, {nombre}!'

@app.route('/about/')
def about():
    # Página "Acerca de"
    return render_template('about.html', title='Acerca de')

# --- Rutas para gestión de productos ---
@app.route('/productos')
def listar_productos():
    # Listar productos, permite búsqueda por nombre usando query string 'q'
    q = request.args.get('q', '').strip()
    productos = inventario.buscar_por_nombre(q) if q else inventario.listar_todos()
    return render_template('products/list.html', title='Productos', productos=productos, q=q)

@app.route('/productos/nuevo', methods=['GET', 'POST'])
def crear_producto():
    # Formulario para crear un nuevo producto
    form = ProductoForm()
    if form.validate_on_submit():
        try:
            inventario.agregar(
                nombre=form.nombre.data,
                cantidad=form.cantidad.data,
                precio=form.precio.data
            )
            flash('Producto agregado correctamente.', 'success')
            return redirect(url_for('listar_productos'))
        except ValueError as e:
            form.nombre.errors.append(str(e))
    return render_template('products/form.html', title='Nuevo producto', form=form, modo='crear')

@app.route('/productos/<int:pid>/editar', methods=['GET', 'POST'])
def editar_producto(pid):
    # Formulario para editar un producto existente
    prod = Producto.query.get_or_404(pid)
    form = ProductoForm(obj=prod)
    if form.validate_on_submit():
        try:
            inventario.actualizar(
                id=pid,
                nombre=form.nombre.data,
                cantidad=form.cantidad.data,
                precio=form.precio.data
            )
            flash('Producto actualizado.', 'success')
            return redirect(url_for('listar_productos'))
        except ValueError as e:
            form.nombre.errors.append(str(e))
    return render_template('products/form.html', title='Editar producto', form=form, modo='editar')

@app.route('/productos/<int:pid>/eliminar', methods=['POST'])
def eliminar_producto(pid):
    # Eliminar un producto por su ID
    ok = inventario.eliminar(pid)
    flash('Producto eliminado.' if ok else 'Producto no encontrado.', 'info' if ok else 'warning')
    return redirect(url_for('listar_productos'))

# Ejecutar la aplicación en modo debug si se llama directamente
if __name__ == '__main__':
    app.run(debug=True)