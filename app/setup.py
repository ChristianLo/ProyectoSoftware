import psycopg2
from config import *

conn = psycopg2.connect("dbname=%s host=%s user=%s password=%s" % (database, host, user, password))

cur = conn.cursor()

# sql = """ DROP SCHEMA public CASCADE;
# CREATE SCHEMA public;
# """

# cur.execute(sql)

sql = """
CREATE TABLE sucursal( id SERIAL PRIMARY KEY , id_adm_local INTEGER , calle VARCHAR, nombre VARCHAR , comuna VARCHAR, ciudad VARCHAR, region VARCHAR, telefono INTEGER);
CREATE TABLE usuario(id SERIAL PRIMARY KEY, tipo VARCHAR, nombre VARCHAR, rut INTEGER, password VARCHAR, telefono INTEGER , email VARCHAR );
CREATE TABLE productos(id SERIAL PRIMARY KEY , nombre VARCHAR , cantidad INTEGER, detalle VARCHAR);
CREATE TABLE ventas(num_venta SERIAL PRIMARY KEY , tipo INTEGER, cliente_id INTEGER, fechahora TIMESTAMP);
CREATE TABLE ventas_detalle(num_venta INTEGER, tipo_compra INTEGER, id_compra INTEGER, monto INTEGER , cantidad INTEGER);
CREATE TABLE cupon(id SERIAL PRIMARY KEY, precio INTEGER, fecha_inicio TIMESTAMP, fecha_termino TIMESTAMP);
CREATE TABLE cupon_detalle(cupon_id INTEGER, producto_id INTEGER, cantidad INTEGER);
CREATE TABLE promocion(id SERIAL PRIMARY KEY, precio INTEGER);
CREATE TABLE promocion_detalle(promo_id INTEGER, producto_id INTEGER, cantidad INTEGER);
"""


def get_email(id):
    try:
        if type(id) is int:
            id = str(id)
        cur.execute("""SELECT email FROM usuario WHERE id = %s""", id)
        email = cur.fetchall()
        if not email:
            return None, 'info'
        return email[0][0], 'success'
    except psycopg2.Error as e:
        print(e)


print(get_email(1))
# queda con 255 el varchar
# cur.execute(sql)
conn.commit()
cur.close()
conn.close()
