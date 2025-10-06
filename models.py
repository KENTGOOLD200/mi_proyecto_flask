from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Inicializamos SQLAlchemy para usarlo en toda la aplicación
db = SQLAlchemy()

# Modelo de producto
class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Identificador único del producto
    nombre = db.Column(db.String(120), unique=True, nullable=False)  # Nombre del producto, debe ser único y no nulo
    imagen = db.Column(db.String(255))  # Ruta o URL de la imagen del producto
    descripcion = db.Column(db.Text)  # Descripción detallada del producto
    categoria = db.Column(db.String(50))  # Categoría principal del producto
    subcategoria = db.Column(db.String(50))  # Subcategoría del producto
    talla = db.Column(db.String(10))  # Talla del producto
    color = db.Column(db.String(30))  # Color del producto
    material = db.Column(db.String(50))  # Material del producto
    cantidad = db.Column(db.Integer, default=0)  # Cantidad disponible en inventario
    precio = db.Column(db.Float, default=0)  # Precio del producto

    def __repr__(self):
        # Representación legible del objeto Producto
        return f'<Producto {self.id} {self.nombre}>'

    def to_tuple(self):
        # Devuelve una tupla con los datos del producto
        return (self.id, self.nombre,self.imagen, self.descripcion, self.categoria, self.subcategoria, self.talla, self.color,self.material, self.cantidad, self.precio)

# Modelo de usuario compatible con Flask-Login
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'  # Nombre de la tabla en la base de datos

    id = db.Column('id_usuario', db.Integer, primary_key=True)  # ID único del usuario
    nombre = db.Column(db.String(100))  # Nombre del usuario
    apellido = db.Column(db.String(100))  # Apellido
    foto =  db.Column(db.String(255)) # Ruta o URL de la foto de perfil
    email = db.Column(db.String(100), unique=True)  # Email único
    telefono = db.Column(db.String(20))  # Número de teléfono
    pais = db.Column(db.String(50))  # País
    ciudad = db.Column(db.String(50))  # Ciudad
    codigo_postal = db.Column(db.String(20))  # Código postal
    password = db.Column(db.String(100))  # Contraseña (debe estar hasheada en producción)

    def __repr__(self): 
        # Representación legible del objeto Usuario
        return f'<Usuario {self.id} {self.nombre} {self.apellido}>'
    def to_tuple(self):
        # Devuelve una tupla con los datos del usuario
        return (self.id, self.nombre, self.apellido,self.foto, self.email, self.telefono, self.pais, self.ciudad, self.codigo_postal, self.password)
