# -*- coding=utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField, IntegerField
from wtforms.validators import *


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class CreateUser(Form):
    username = StringField('Username', validators=[Length(min=4, max=25)])
    password = PasswordField('New Password', validators=[
        DataRequired(),
        EqualTo('confim', message='Password must match')])
    confirm = PasswordField('Repeat Password')
    nombre = StringField('Nombre', validators=[DataRequired()])
    rut = IntegerField('Rut', validators=[DataRequired()])
    telefono = IntegerField('Telefono', validators=[DataRequired()])
    correo = StringField('Email', validators=[Length(min=6, max=35), Email()])

