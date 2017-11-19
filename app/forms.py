from flask_wtf import Form
from wtforms import StringField, BooleanField, PasswordField
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
    correo = StringField('Email', validators=[Length(min=6, max=35), Email()])

