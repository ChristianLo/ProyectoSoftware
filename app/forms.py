# -*- coding=utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, IntegerField, SelectField
from wtforms.validators import *


class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(message='Campo requerido')])
    password = PasswordField('password', validators=[DataRequired(message='Campo requerido')])
    remember_me = BooleanField('remember_me', default=False)


class CreateUser(FlaskForm):
    username = StringField('Username', validators=[
        Length(min=4, max=25, message='Usuario debe tener 4 o mas caracteres')
    ])
    password = PasswordField('New Password', validators=[
        Length(min=6, max=25, message='Contraseña debe tener 6 o mas caracteres'),
        DataRequired(message='Campo requerido'),
        EqualTo('confirm', message='Contraseña no compatible')
    ])
    confirm = PasswordField('Repeat Password')
    nombre = StringField('Nombre', validators=[
        DataRequired(message='Campo requerido')
    ])
    rut = IntegerField('Rut', validators=[
        DataRequired(message='Campo requerido', )
    ])
    telefono = StringField('Celular', validators=[
        Length(min=8, max=8, message='Numero no valido'),
        DataRequired(message='Campo requerido')
    ])
    correo = StringField('Email', validators=[
        Length(min=6, max=35, message='Correo no valido'),
        Email(message='Correo no valido')
    ])



