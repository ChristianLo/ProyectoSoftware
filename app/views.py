# -*- coding=utf-8 -*-

import datetime

import psycopg2
from flask import flash, redirect, request, url_for, session
from mercadopago import MP

from app import app, templates
from .config import *
from .forms import CreateUser, LoginForm

conn = psycopg2.connect("dbname=%s host=%s user=%s password=%s" %
                        (database, host, user, password))  # type: psycopg2.extensions.connection


cur = conn.cursor()

CLIENT_ID = '553621602157005'
CLIENT_SECRET = 'op1Jwd2cQAjGTQ19b9TcqrtSaPTzgwT6'
ACCESS_TOKEN = 'TEST-553621602157005-111721-95bf394d8b38f589054abe1d4fca99d4__LB_LA__-189487427'
PUBLIC_KEY = 'TEST-13c0f310-c9fa-464c-b7ac-3f75c749f8ca'

mp = MP(CLIENT_ID, CLIENT_SECRET)


def errores(form):
    for field, error in form.errors.items():
        flash(field.capitalize() + ': ' + '\n'.join(error), category='danger')


@app.route('/')
@app.route('/index')
@templates('index.html')
def index():
    pass


@app.route('/menu')
@templates('menu.html')
def menu():
    # fotos o imagenes y datos del menu
    pass


@app.route('/compra')
@templates('compra.html')
def compra():
    productos, message = get_productos(all=True)
    if productos == (None, 'info'):
        flash('Error en cargar', category='info')
        pass
    else:
        return dict(productos=productos)


@app.route('/contacto')
@templates('contacto.html')
def contacto():
    # datos de cada sucursal donde se encuentran
    pass


# ------------------------- Comprar cupon y verficar pago de cupon ---------------

@app.route('/pago', methods=['POST'])
def pago():
    # id hace referencia al producto a comprar y obtener
    # como: nombre, valor, precio unitario

    if request.method == 'POST' and session['user']:
        datos, message = get_productos(nombre=request.form['producto'], id=True)
        if datos is None and message is 'info':
            flash('Producto no encontrado', category=message)
            return redirect(url_for('compra'))

        preference = {
            'items': [
                {
                    'id': datos[0],
                    'title': datos[1],
                    'quantity': int(request.form['cantidad']),  # dado que se compra un cupon
                    'curreny_id': 'CLP',
                    'unit_price': int(datos[2])
                }
            ],
        }

        preferenceResult = mp.create_preference(preference)

        url = preferenceResult['response']['init_point']
        return redirect(url)
    pass


@app.route('/verificar_pagos')
def verficar_pagos():
    # mp = MP(ACCESS_TOKEN)
    if session['gerente_sucursal']:
        lista_pagos = []
        payment = mp.get('/v1/payments/search')
        obtener = request.form['correo']  # obtenre correo por id de usuario
        for k in payment['results']:
            if obtener is k['payer']['email']:
                lista_pagos.append(k)
                flash(k['status'], category='info')
        if len(lista_pagos) < 1:
            flash('No se han encotrado pagos de este correo', category='warning')
        redirect(url_for('compra'))

    redirect(url_for('index'))


# ---------------------------- Metodos de ingresar y salir del sistema -----------
@app.route('/login', methods=['GET', 'POST'])
@templates('login.html')
def login():
    error = None
    form = LoginForm(request.form)
    if request.method == 'POST':
        if not form.validate_on_submit():
            errores(form)
        else:
            datos, tipo = get_user(form.data['username'], form.data['password'])
            print(datos, tipo)
            if type(datos) is tuple and tipo:
                if datos[1] is '1':
                    session['admin'] = True
                elif datos[1] is '2':
                    session['gerente'] = True
                elif datos[1] is '3':
                    session['gerente_sucursal'] = True
                    session['id'] = datos[2]
                session['user'] = True
                flash('Ha iniciado correctamente.', 'success')
                return redirect(url_for('index'))
            flash(datos, category=tipo)
    return dict(form=form)


@app.route('/logout')
def logout():
    session.pop('admin', None)
    session.pop('user', None)
    session.pop('gerente', None)
    session.pop('gerente_sucursal', None)
    flash('se ha cerrado sesion.', category='success')
    return redirect(url_for('index'))


# -------------------- Creacion de usuario ------------------------

@app.route('/create', methods=['GET', 'POST'])
@templates('create.html')
def create():
    form = CreateUser(request.form)
    if request.method == 'POST':
        # funcion para recibir datos de usuario
        print(form.data)
        if form.validate():
            mensaje, tipo = insert_usuario(
                form.data['username'],
                form.data['nombre'],
                form.data['rut'],
                form.data['password'],
                form.data['telefono'],
                form.data['correo'])
            flash(mensaje, category=tipo)
            return redirect(url_for('login'))
        errores(form)
    return dict(form=form)


# ---------------------

@app.route('/generar_informe')
@templates('informe.html')
def generar_informe():
    pass


@app.route('/gestionar')
@templates('gestionar.html')
def gestionar():
    pass


# --------------------------- funciones ------------------------------

def insert_usuario(nickname, nombre, rut, password, telefono, email):
    try:

        cur.execute("""
        INSERT INTO usuario (tipo, username, nombre, rut, password, telefono, email)
        VALUES ('5', %s, %s, %s, %s, %s, %s);
        """, (str(nickname), str(nombre), str(rut), str(password), str(telefono), str(email)))
        conn.commit()
        return 'Usuario creado', 'success'
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
        return 'No se ha podido crear', 'info'


def get_cupon():
    cupones = None
    productos = None
    try:
        cur.execute("""SELECT id, precio FROM cupon""")
        cupones = cur.fetchall()
        cur.execute("""
        SELECT productos FROM cupon_detalle 
        WHERE cupon_id = (SELECT id FROM cupon)"""
                    )
        productos = cur.fetchall()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if cupones and productos:
            return dict(cupones=cupones, productos=productos)
        return 'cupones no disponible', 'info'


def get_productos(nombre='-1', all=False, id=False):
    productos = None
    try:
        if all:
            cur.execute("""SELECT nombre, cantidad, detalle FROM productos""")
            productos = cur.fetchall()
        if id == '-1':
            cur.execute("""SELECT nombre, detalle FROM  productos""")
            productos = cur.fetchone()
        elif nombre and id:
            cur.execute("""SELECT id, nombre, cantidad FROM productos""")
            productos = cur.fetchone()
        else:
            cur.execute("""SELECT nombre, detalle FROM productos WHERE nombre = %s""", nombre)
            productos = cur.fetchone()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if not productos:
            return None, 'info'
        return productos, True


def get_user(username, password):
    accept = None
    try:
        cur.execute("""
        SELECT nombre, tipo, id FROM usuario 
        WHERE username = %s AND password = %s""",
                    (username, password))
        accept = cur.fetchone()
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if accept:
            return accept, True
        return 'Usuario o contraseña incorrecta', 'danger'


def get_ventas(id):
    try:
        fecha_hoy = datetime.datetime.now()
        fecha_inicio = datetime.datetime(
            fecha_hoy.year,
            fecha_hoy.month,
            1,  # dia
            0,  # hora
            0  # minutos
        )
        cur.execute("""

        """)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
