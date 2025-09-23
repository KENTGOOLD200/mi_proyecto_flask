from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Inicializamos SQLAlchemy para usarlo en toda la aplicación
db = SQLAlchemy()

# Modelo de productos para el inventario
class Producto(db.Model):
    __tablename__ = 'productos'  # Nombre de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)  # ID único del producto
    nombre = db.Column(db.String(120), unique=True, nullable=False)  # Nombre único
    cantidad = db.Column(db.Integer, nullable=False, default=0)  # Cantidad disponible
    precio = db.Column(db.Float, nullable=False, default=0.0)  # Precio unitario

    def __repr__(self):
        return f'<Producto {self.id} {self.nombre}>'

    def to_tuple(self):
        # Devuelve una tupla con los datos del producto
        return (self.id, self.nombre, self.cantidad, self.precio)

# Modelo de usuario compatible con Flask-Login
class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuarios'  # Nombre de la tabla en la base de datos

    id = db.Column('id_usuario', db.Integer, primary_key=True)  # ID único del usuario
    nombre = db.Column(db.String(100))  # Nombre del usuario
    apellido = db.Column(db.String(100))  # Apellido
    email = db.Column(db.String(100), unique=True)  # Email único
    telefono = db.Column(db.String(20))  # Número de teléfono
    pais = db.Column(db.String(50))  # País
    ciudad = db.Column(db.String(50))  # Ciudad
    codigo_postal = db.Column(db.String(20))  # Código postal
    password = db.Column(db.String(100))  # Contraseña (debe estar hasheada en producción)
