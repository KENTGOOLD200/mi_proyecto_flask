from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, PasswordField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, Email, EqualTo
from wtforms.fields import EmailField

# Formulario para productos
class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=120)])
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
