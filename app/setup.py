# -*- coding=utf-8 -*-

import datetime

import psycopg2

from .config import *

conn = psycopg2.connect("dbname=%s host=%s user=%s password=%s" %
                        (database, host, user, password))  # type: psycopg2.extensions.connection

cur = conn.cursor()  # type: psycopg2.extensions.cursor

# sql = """ DROP SCHEMA public CASCADE;
# CREATE SCHEMA public;
# """

# cur.execute(sql)

sql = """
CREATE TABLE sucursal( id SERIAL PRIMARY KEY , id_adm_local INTEGER , calle VARCHAR, nombre VARCHAR , comuna VARCHAR, ciudad VARCHAR, region VARCHAR, telefono INTEGER);
CREATE TABLE usuario(id SERIAL PRIMARY KEY, tipo VARCHAR, nombre VARCHAR, rut INTEGER, password VARCHAR, telefono INTEGER , email VARCHAR, nickname VARCHAR() );
CREATE TABLE productos(id SERIAL PRIMARY KEY , nombre VARCHAR , cantidad INTEGER, detalle VARCHAR);
CREATE TABLE ventas(num_venta SERIAL PRIMARY KEY , tipo INTEGER, cliente_id INTEGER, fechahora TIMESTAMP);
CREATE TABLE ventas_detalle(num_venta INTEGER, tipo_compra INTEGER, id_compra INTEGER, monto INTEGER , cantidad INTEGER);
CREATE TABLE cupon(id SERIAL PRIMARY KEY, precio INTEGER, fecha_inicio TIMESTAMP, fecha_termino TIMESTAMP);
CREATE TABLE cupon_detalle(cupon_id INTEGER, producto_id INTEGER, cantidad INTEGER);
CREATE TABLE promocion(id SERIAL PRIMARY KEY, precio INTEGER);
CREATE TABLE promocion_detalle(promo_id INTEGER, producto_id INTEGER, cantidad INTEGER);
"""


def closed():
    status = cur.connection


def insert_usuario(nickname, nombre, rut, password, telefono, email):
    try:
        cur.execute("""
        INSERT INTO usuario (tipo, username, nombre, rut, password, telefono, email)
        VALUES ('5', %s, %s, %s, %s, %s, %s);
        """, (nickname, nombre, rut, password, telefono, email))
        conn.commit()
        return 'Usuario creado', 'success'
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)


def get_cupon():
    try:
        cur.execute("""SELECT id, precio FROM cupon""")
        cupones = cur.fetchall()
        cur.execute("""
        SELECT productos FROM cupon_detalle 
        WHERE cupon_id = (SELECT id FROM cupon)"""
                    )
        productos = cur.fetchall()
        if cupones and productos:
            return dict(cupones=cupones, productos=productos)
        return 'cupones no disponible', 'info'
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_productos(id='-1', all=False):
    try:
        if all:
            cur.execute("""SELECT * FROM productos""")
            return cur.fetchall()
        if id == '-1':
            cur.execute("""SELECT nombre, detalle FROM  productos""")
            productos = cur.fetchone()
        else:
            cur.execute("""SELECT nombre, detalle FROM productos WHERE id = %s""", id)
            productos = cur.fetchone()
        if not productos:
            return None, 'info'
        return productos, True

    except(Exception, psycopg2.DatabaseError) as error:
        print(error)


def get_user(username, password):
    try:
        cur.execute("""
        SELECT nombre, tipo, id FROM usuario 
        WHERE username = %s AND password = %s""",
                    (username, password))
        accept = cur.fetchone()
        if accept:
            return accept, True
        return 'error', 'danger'
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)


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


conn.commit()
cur.closed()
conn.closed()
