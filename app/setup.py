from config import *
import psycopg2
conn = psycopg2.connect("dbname=%s host=%s user=%s password=%s"%(database,host,user,password))

cur = conn.cursor()

# sql = """ DROP SCHEMA public CASCADE;
# CREATE SCHEMA public;
# """

# cur.execute(sql)

sql = """
CREATE TABLE sucursal( id serial PRIMARY KEY , id_adm_local integer , calle varchar, nombre varchar , comuna varchar, ciudad varchar, region varchar, telefono integer);
CREATE TABLE usuario(id serial PRIMARY KEY, tipo varchar, nombre varchar, rut integer, password varchar, telefono integer , email varchar );
CREATE TABLE productos(id serial PRIMARY KEY , nombre varchar , cantidad integer, detalle varchar);
CREATE TABLE ventas(num_venta serial PRIMARY KEY , tipo integer, cliente_id integer, fechahora timestamp);
CREATE TABLE ventas_detalle(num_venta integer, tipo_compra integer, id_compra integer, monto integer , cantidad integer);
CREATE TABLE cupon(id serial PRIMARY KEY, precio integer, fecha_inicio timestamp, fecha_termino timestamp);
CREATE TABLE cupon_detalle(cupon_id integer, producto_id integer, cantidad integer);
CREATE TABLE promocion(id serial PRIMARY KEY, precio integer);
CREATE TABLE promocion_detalle(promo_id integer, producto_id integer, cantidad integer);
"""

#queda con 255 el varchar
cur.execute(sql)
conn.commit()
cur.close()
conn.close()
