from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DecimalField, PasswordField, SubmitField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired, NumberRange, Length, Email, EqualTo
from wtforms.fields import EmailField
from werkzeug.utils import secure_filename

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, DecimalField, SubmitField, FileField
from wtforms.validators import DataRequired, Length, NumberRange, Regexp
from flask_wtf.file import FileAllowed

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[
        DataRequired(message="El nombre del producto es obligatorio."),
        Length(max=120, message="El nombre no debe superar los 120 caracteres.")
    ])

    imagen = FileField('Imagen', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Solo se permiten imágenes en formato JPG, JPEG, PNG o GIF.')
    ])

    descripcion = TextAreaField('Descripción', validators=[
        Length(max=1000, message="La descripción no debe superar los 1000 caracteres.")
    ])

    categoria = StringField('Categoría', validators=[
        Length(max=50, message="La categoría no debe superar los 50 caracteres."),
        Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]*$', message="La categoría solo debe contener letras.")
    ])

    subcategoria = StringField('Subcategoría', validators=[
        Length(max=50, message="La subcategoría no debe superar los 50 caracteres."),
        Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]*$', message="La subcategoría solo debe contener letras.")
    ])

    talla = StringField('Talla', validators=[
        Length(max=10, message="La talla no debe superar los 10 caracteres."),
        Regexp(r'^[a-zA-Z0-9\s\-]*$', message="La talla solo puede contener letras, números y guiones.")
    ])

    color = StringField('Color', validators=[
        Length(max=30, message="El color no debe superar los 30 caracteres."),
        Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]*$', message="El color solo debe contener letras.")
    ])

    material = StringField('Material', validators=[
        Length(max=50, message="El material no debe superar los 50 caracteres."),
        Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]*$', message="El material solo debe contener letras.")
    ])

    cantidad = IntegerField('Cantidad', validators=[
        DataRequired(message="La cantidad es obligatoria."),
        NumberRange(min=0, message="La cantidad no puede ser negativa.")
    ])

    precio = DecimalField('Precio', places=2, validators=[
        DataRequired(message="El precio es obligatorio."),
        NumberRange(min=0, message="El precio no puede ser negativo.")
    ])

    submit = SubmitField('Guardar')

# Formulario de inicio de sesión
from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = EmailField('Correo electrónico', validators=[
        DataRequired(message="El correo electrónico es obligatorio."),
        Email(message="Introduce un correo electrónico válido.")
    ])
    
    password = PasswordField('Contraseña', validators=[
        DataRequired(message="La contraseña es obligatoria.")
    ])
    
    submit = SubmitField('Iniciar sesión')

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField
from wtforms.fields import EmailField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Regexp
from flask_wtf.file import FileAllowed

# Formulario de registro de usuario
class RegisterForm(FlaskForm):
    nombre = StringField('Nombre', validators=[
        DataRequired(message="El nombre es obligatorio."),
        Length(max=100, message="El nombre no debe superar los 100 caracteres."),
        Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', message="El nombre solo debe contener letras.")
    ])
    
    apellido = StringField('Apellido', validators=[
        DataRequired(message="El apellido es obligatorio."),
        Length(max=100, message="El apellido no debe superar los 100 caracteres."),
        Regexp(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', message="El apellido solo debe contener letras.")
    ])
    
    foto = FileField('Foto de perfil', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Solo se permiten imágenes en formato JPG, JPEG, PNG o GIF.')
    ])
    
    email = EmailField('Correo electrónico', validators=[
        DataRequired(message="El correo electrónico es obligatorio."),
        Email(message="Introduce un correo electrónico válido."),
        Length(max=100, message="El correo no debe superar los 100 caracteres.")
    ])
    
    telefono = StringField('Teléfono', validators=[
        DataRequired(message="El número de teléfono es obligatorio."),
        Regexp(r'^\d{10}$', message="El número de teléfono debe tener exactamente 10 dígitos.")
    ])
    
    pais = StringField('País', validators=[
        DataRequired(message="El país es obligatorio."),
        Length(max=50, message="El país no debe superar los 50 caracteres.")
    ])
    
    ciudad = StringField('Ciudad', validators=[
        DataRequired(message="La ciudad es obligatoria."),
        Length(max=50, message="La ciudad no debe superar los 50 caracteres.")
    ])
    
    codigo_postal = StringField('Código Postal', validators=[
        DataRequired(message="El código postal es obligatorio."),
        Regexp(r'^\d+$', message="El código postal debe contener solo números."),
        Length(max=20, message="El código postal no debe superar los 20 caracteres.")
    ])
    
    password = PasswordField('Contraseña', validators=[
        DataRequired(message="La contraseña es obligatoria."),
        Length(min=8, message="La contraseña debe tener al menos 8 caracteres."),
        Regexp(r'.*[A-Z].*', message="La contraseña debe contener al menos una letra mayúscula."),
        Regexp(r'.*\d.*', message="La contraseña debe contener al menos un número.")
    ])
    
    confirm_password = PasswordField('Confirmar contraseña', validators=[
        DataRequired(message="Confirma tu contraseña."),
        EqualTo('password', message='Las contraseñas no coinciden.')
    ])
    
    submit = SubmitField('Registrarse')
