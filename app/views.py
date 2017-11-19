from flask import flash, redirect, request, url_for, session, json
from mercadopago import MP

from app import app, templates
from .forms import CreateUser
from .setup import *

CLIENT_ID = '553621602157005'
CLIENT_SECRET = 'op1Jwd2cQAjGTQ19b9TcqrtSaPTzgwT6'
ACCESS_TOKEN = 'TEST-553621602157005-111721-95bf394d8b38f589054abe1d4fca99d4__LB_LA__-189487427'
PUBLIC_KEY = 'TEST-13c0f310-c9fa-464c-b7ac-3f75c749f8ca'

mp = MP(CLIENT_ID, CLIENT_SECRET)
mp.sandbox_mode(True)


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
    # cupones disponibles
    pass


@app.route('/contacto')
@templates('contacto.html')
def contacto():
    # datos de cada sucursal donde se encuentran
    pass


@app.route('/contact')
@templates('contact.html')
def contact():
    pass


# ------------------------- Comprar cupon y verficar pago de cupon ---------------

@app.route('/pago/<id>', methods=['POST', 'GET'])
def pago(id):
    # id hace referencia al producto a comprar y obtener
    # como: nombre, valor, precio unitario
    """
    preference = {
        'items': [
            {
                'id': id_cupon
                'title': nombre_produto
                'quantity: 1  # dado que se compra un cupon
                'curreny_id': 'CLP'
                'unit_price': precio
            }
        ],
        'payer': {
            'name': 'username'
            'email: user_email
        }
        'expires': true
    }
    """

    preference = {
        "items": [
            {
                "title": "HandsRolls",
                "quantity": 1,
                "currency_id": "CLP",  # Available currencies at: https://api.mercadopago.com/currencies
                "unit_price": 2000.0
            }
        ]
    }
    preferenceResult = mp.create_preference(preference)

    url = preferenceResult['response']['init_point']
    return redirect(url)


@app.route('/verificar_pagos/<id>')
def verficar_pagos(id: int):
    # mp = MP(ACCESS_TOKEN)
    if session['admin'] == 'vendedor':
        lista_pagos = []
        payment = mp.get('/v1/payments/search')
        obtener = "correo"  # obtenre correo por id de usuario
        for k in payment['results']:
            if obtener is k['payer']['email']:
                lista_pagos.append(k)
                flash(k['status'], category='info')
        if len(lista_pagos) < 1:
            flash('No se han encotrado pagos de este correo', category='warning')
        redirect(url_for('compra'))

    redirect(url_for('index'))


# ----------------------------------- Metodos de ingresar y salir del sistema

@app.route('/login', methods=['GET', 'POST'])
@templates('login.html')
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or \
                        request.form['password'] != 'secret':
            error = 'Email incorrecto o contraseña incorrecta.'
        else:
            flash('Has accesido correctamente.', category='success')
            session['admin'] = request.form['username']
            session['user'] = 'admin'
            return redirect(url_for('index'))
    return dict(error=error)


@app.route('/logout')
def logout():
    session.pop('admin', None)
    session.pop('user', None)
    flash('se ha cerrado sesion.', category='success')
    return redirect(url_for('index'))


# -------------------- Creacion de usuario ------------------------

@app.route('/create', methods=['GET', 'POST'])
@templates('create.html')
def create():
    form = CreateUser(request.form)
    if request.method == 'POST' and form.validate():
        # funcion para recibir datos de usuario
        mensaje, tipo = insert_usuario(*form.data)
        return redirect(url_for('login'))
    return dict(form=form)
