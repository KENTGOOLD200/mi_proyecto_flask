# Importa la clase base para formularios de Flask-WTF
from flask_wtf import FlaskForm
# Importa los tipos de campos que se usarán en el formulario
from wtforms import StringField, IntegerField, DecimalField, SubmitField
# Importa los validadores para los campos del formulario
from wtforms.validators import DataRequired, NumberRange, Length

# Define una clase de formulario para productos
class ProductoForm(FlaskForm):
    # Campo de texto para el nombre del producto, obligatorio y con máximo 120 caracteres
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=120)])
    # Campo numérico entero para la cantidad, obligatorio y no puede ser negativo
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=0)])
    # Campo numérico decimal para el precio, obligatorio y no puede ser negativo, con 2 decimales
    precio = DecimalField('Precio', places=2, validators=[DataRequired(), NumberRange(min=0)])
    # Botón para enviar el formulario
    submit = SubmitField('Guardar')
