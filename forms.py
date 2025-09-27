from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, PasswordField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, NumberRange, Length, Email, EqualTo
from wtforms.fields import EmailField
from werkzeug.utils import secure_filename

# Formulario para productos

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=120)])
    imagen = FileField('Imagen', validators=[FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Solo se permiten imágenes.')])
    descripcion = TextAreaField('Descripción')
    categoria = StringField('Categoría)', validators=[Length(max=50)])
    subcategoria = StringField('Subcategoría', validators=[Length(max=50)])
    talla = StringField('Talla', validators=[Length(max=10)])
    color = StringField('Color', validators=[Length(max=30)])
    material = StringField('Material', validators=[Length(max=50)])
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=0)])
    precio = DecimalField('Precio', places=2, validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Guardar')


# Formulario de inicio de sesión
class LoginForm(FlaskForm):
    email = EmailField('Correo electrónico', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión')

# Formulario de registro de usuario
class RegisterForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=100)])
    email = EmailField('Correo electrónico', validators=[DataRequired(), Email(), Length(max=100)])
    telefono = StringField('Teléfono', validators=[DataRequired(), Length(max=20)])
    pais = StringField('País', validators=[DataRequired(), Length(max=50)])
    ciudad = StringField('Ciudad', validators=[DataRequired(), Length(max=50)])
    codigo_postal = StringField('Código Postal', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        'Confirmar contraseña',
        validators=[DataRequired(), EqualTo('password', message='Las contraseñas no coinciden.')]
    )
    submit = SubmitField('Registrarse')
