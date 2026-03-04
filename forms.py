from wtforms import Form
from wtforms import StringField, IntegerField, PasswordField
from wtforms import EmailField
from wtforms import validators

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, EmailField
from wtforms.validators import DataRequired, Length, Email

class UserForm(Form):

    
    nombre=StringField('Nombre', [
        validators.DataRequired(message="El campo es requerido"),
        validators.Length(min=4,max=10,message="Ingresa nombre valido")
    ])
    apaterno=StringField('aPaterno',[
        validators.DataRequired(message="El campo es requerido"),

    ])
    email=EmailField('Correo',[
        validators.email(message="Ingrese un correo valido"),

    ])

class MaestroForm(FlaskForm):

    matricula = IntegerField(
        'Matrícula',
        validators=[DataRequired(message='La Matrícula es requerida')]
    )

    nombre = StringField(
        'Nombre',
        validators=[DataRequired(message='El Nombre es requerido')]
    )

    apaterno = StringField(   # 🔥 CAMBIADO (antes apellidos)
        'Apellido Paterno',
        validators=[DataRequired(message='El Apellido Paterno es requerido')]
    )

    especialidad = StringField(
        'Especialidad',
        validators=[DataRequired(message='La Especialidad es requerida')]
    )

    email = StringField(
        'Email',
        validators=[
            DataRequired(message='El correo es requerido'),
            Email(message='Ingrese un correo válido')
        ]
    )