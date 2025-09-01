from flask_sqlalchemy import SQLAlchemy

# Se crea una instancia de SQLAlchemy para manejar la base de datos
db = SQLAlchemy()

# Definición del modelo Producto, que representa la tabla 'productos' en la base de datos
class Producto(db.Model):
    __tablename__ = 'productos'  # Nombre de la tabla en la base de datos

    # Definición de las columnas de la tabla
    id = db.Column(db.Integer, primary_key=True)  # Identificador único del producto
    nombre = db.Column(db.String(120), unique=True, nullable=False)  # Nombre del producto, debe ser único y no nulo
    cantidad = db.Column(db.Integer, nullable=False, default=0)  # Cantidad disponible, no puede ser nulo, valor por defecto 0
    precio = db.Column(db.Float, nullable=False, default=0.0)  # Precio del producto, no puede ser nulo, valor por defecto 0.0

    def __repr__(self):
        # Representación en texto del objeto Producto, útil para depuración
        return f'<Producto {self.id} {self.nombre}>'

    def to_tuple(self):
        # Devuelve una tupla con los datos principales del producto
        # Ejemplo de tupla: (id, nombre, cantidad, precio)
        return (self.id, self.nombre, self.cantidad, self.precio)
