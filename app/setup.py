# -*- coding=utf-8 -*-

import datetime

import psycopg2

from .config import *

conn = psycopg2.connect("dbname=%s host=%s user=%s password=%s" %
                        (database, host, user, password))  # type: psycopg2.extensions.connection

cur = conn.cursor()  # type: psycopg2.extensions.cursor

sql = """ DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
"""

cur.execute(sql)
sql = """
IF NOT EXISTS sucursal CREATE TABLE sucursal( id SERIAL PRIMARY KEY , id_adm_local INTEGER , calle VARCHAR, nombre VARCHAR , comuna VARCHAR, ciudad VARCHAR, region VARCHAR, telefono INTEGER);
IF NOT EXISTS usuario CREATE TABLE usuario(id SERIAL PRIMARY KEY, tipo VARCHAR, nombre VARCHAR, rut INTEGER, password VARCHAR, telefono INTEGER , email VARCHAR, nickname VARCHAR() );
IF NOT EXISTS productos CREATE TABLE productos(id SERIAL PRIMARY KEY , nombre VARCHAR , cantidad INTEGER, detalle VARCHAR);
IF NOT EXISTS ventas CREATE TABLE ventas(num_venta SERIAL PRIMARY KEY , tipo INTEGER, cliente_id INTEGER, fechahora TIMESTAMP);
IF NOT EXISTS ventas_detalle CREATE TABLE ventas_detalle(num_venta INTEGER, tipo_compra INTEGER, id_compra INTEGER, monto INTEGER , cantidad INTEGER);
IF NOT EXISTS cupon CREATE TABLE cupon(id SERIAL PRIMARY KEY, precio INTEGER, fecha_inicio TIMESTAMP, fecha_termino TIMESTAMP);
IF NOT EXISTS cupon_detalle CREATE TABLE cupon_detalle(cupon_id INTEGER, producto_id INTEGER, cantidad INTEGER);
IF NOT EXISTS promocion CREATE TABLE promocion(id SERIAL PRIMARY KEY, precio INTEGER);
IF NOT EXISTS promocion_detalle CREATE TABLE promocion_detalle(promo_id INTEGER, producto_id INTEGER, cantidad INTEGER);
"""

try:
    cur.execute(sql)
except psycopg2.ProgrammingError:
    pass

sql = """
INSERT INTO productos
(nombre, cantidad, detalle)
VALUES ('Gyosas de camaron', 2200, '5 unidades');
INSERT INTO productos
(nombre, cantidad, detalle)
VALUES ('Gyosas de pollo', 2400, '5 unidades');
INSERT INTO productos
(nombre, cantidad, detalle)
VALUES ('Gyosas de Cerdo', 2000, '5 unidades');
INSERT INTO productos
(nombre, cantidad, detalle)
VALUES ('Ceviche de Camaron', 5500, 'Camarón, lechuga, palta, papa hilo, aderezo de coco');
INSERT INTO productos
(nombre, cantidad, detalle)
VALUES ('Ceviche de Salmon', 5500, 'Salmon, lechuga, palta, papa hilo, aderezo rocato');
INSERT INTO productos
(nombre, cantidad, detalle)
VALUES ('Salmon - Pulpo', 4200, '6 cortes');
INSERT INTO productos
(nombre, cantidad, detalle)
VALUES ('Salmon - Pulpo', 5700, '12 cortes');
INSERT INTO productos
(nombre, cantidad, detalle)
VALUES ('Nigiri', 1900, '2 Bocados de arroz cubierto (salmon - camaron - kanikama - palta');
INSERT INTO productos
(nombre, cantidad, detalle)
VALUES ('Temaki Mixto', 2900, 'Queso, cebollin, salmon, camaron, palta, kanikama, masago');
INSERT INTO productos
(nombre, cantidad, detalle)
VALUES ('Camarones Furai o Tempura', 3800, '6 camarones fritos en Tempura o Panko');
INSERT INTO productos
(nombre, cantidad, detalle)
VALUES ('Tori Rolls', 4200, 'Salmon, queso crema, camarón, envuelto en pollo y frito en panki');
INSERT INTO productos
(nombre, cantidad, detalle)
VALUES ('Esp. Sake Furai', 3900, 'Kamikama, queso crema, pollo, cebollin envuelto en nori y salmon apanado');
INSERT INTO productos
(nombre, cantidad, detalle)
VALUES ('Sakepanko Rolls', 4200, 'Camaron, queso crema, aceitunas, envuelto en salmon y frito en panko');
INSERT INTO productos
(nombre, cantidad, detalle)
VALUES ('Hosomaki Tempura', 3900, 'Camaron, queso crema, envuelto en Nori y frito en Tempura');
INSERT INTO productos
(nombre, cantidad, detalle)
VALUES ('Beef Furai', 4200, 'Queso crema, cebollin, champiñion, envuelto en carne y frito de panko');
INSERT INTO productos
(nombre, cantidad, detalle)
VALUES ('Mozarella Furay', 4200, 'pollo, mozarella, ciboulette, envuelto en pollo y frito en panko');
INSERT INTO productos
(nombre, cantidad, detalle)
VALUES ('Furai', 4200, 'Camaron, queso crema, ciboulette, envuelto en masa tempura');
INSERT INTO productos
(nombre, cantidad, detalle)
VALUES ('Tempura Spicy', 4200, 'Salmon, kanikama, cebollin, salsa spicy, envuelto en masa tempura')
"""

try:
    cur.execute(sql)
except psycopg2.ProgrammingError:
    pass

sql = """
INSERT INTO usuario (id, username, tipo, nombre, rut, password, telefono, email) 
VALUES (1, 'super_user', '1', 'admin', 1, 'yunk7o9', '321', 'admin@mail.cl');
INSERT INTO usuario (id, username, tipo, nombre, rut, password, telefono, email) 
VALUES (2, 'vendedor', '4', 'vendedor', 4, 'g4e3n2', '32121', 'vendedor@mail.cl');
INSERT INTO usuario (id, username, tipo, nombre, rut, password, telefono, email) 
VALUES (3, 'administrador', '3', 'administrador', 2, 'g4e3n2', '3313413', 'administrador@mail.cl')
"""


try:
    cur.execute(sql)
except psycopg2.ProgrammingError:
    pass

conn.commit()
cur.closed()
conn.closed()
