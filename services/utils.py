import psycopg2
import sqlite3
import hashlib
import os

def get_db_connection():
    conn = psycopg2.connect(
        host="bbpzwcbmdyu2wotib6og-postgresql.services.clever-cloud.com",
        port="5432",
        dbname="bbpzwcbmdyu2wotib6og",
        user="uwnuqyetyjpariikmobj",
        password="Is7jUIMZs9x9QLc93kd6WuHIw85Et4"
    )
    return conn

def sha1_hash(password):
    password_bytes = password.encode('utf-8')
    sha1 = hashlib.sha1()
    sha1.update(password_bytes)
    hashed_password = sha1.hexdigest()

    return hashed_password




def str_bus_format(data, service_name=''):
    total_digits = 5

    transformed_data = str(data)

    transformed_data_len = len(transformed_data)

    digits_left = total_digits - len(str(transformed_data_len))

    str_data_lenght = ''

    for i in range(digits_left):
        str_data_lenght += '0'

    str_data_lenght += str(transformed_data_len) + \
        service_name+transformed_data

    return str_data_lenght


def remove_db():
    try:
        os.remove('db.sqlite3')
    except:
        pass


def insert_user(nombre, apellido, email, password, tipo_usuario):
    conn = psycopg2.connect(
        host="bbpzwcbmdyu2wotib6og-postgresql.services.clever-cloud.com",
        port="5432",
        dbname="bbpzwcbmdyu2wotib6og",
        user="uwnuqyetyjpariikmobj",
        password="Is7jUIMZs9x9QLc93kd6WuHIw85Et4"
    )
    c = conn.cursor()

    #Buscar el suario en la db
    c.execute(
        '''SELECT 1 FROM usuarios WHERE correo = %s ''',
        (email,)
    )
    conn.commit()
    user = c.fetchone()
    
    #Si no existe el usuario hacer insert
    if user is None:
        c.execute(
            '''INSERT INTO usuarios (nombre, apellido, correo, contrasena, tipousuario) VALUES (%s, %s, %s, %s, %s)''',
            (nombre, apellido, email, password, tipo_usuario)
        )
        
        conn.commit()
        conn.close()
        
        return True

    else: 
        conn.close()
        return False


def insert_maquinaria(nombre, estado, costo):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''INSERT INTO maquinarias(nombre, estado, costo) VALUES(?, ?, ?)''',
        (nombre, estado, costo)
    )

    conn.commit()
    conn.close()


def consulta_maquinaria(id_maquinaria=''):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    if id_maquinaria == '':
        c.execute('''SELECT * FROM maquinarias''')
    else:
        c.execute(
            '''SELECT * FROM maquinarias WHERE id= ?''', (id_maquinaria,))
    res = c.fetchall()
    conn.commit()
    conn.close()
    return res


def update_maquinaria(id_maquinaria, nombre, estado, costo):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''UPDATE maquinarias SET nombre= ?, estado= ?, costo= ? WHERE id= ?''',
        (nombre, estado, costo, id_maquinaria)
    )

    conn.commit()
    conn.close()
    return c.rowcount


def delete_maquinaria(id_maquinaria):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''UPDATE maquinarias SET fecha_salida=CURRENT_DATE WHERE id= ?''',
        (id_maquinaria)
    )

    conn.commit()
    conn.close()
    return c.rowcount


def insert_componente(id_maquinaria, nombre, estado, marca, modelo, costo):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''INSERT INTO componentes(id_maquinaria, nombre, estado, marca, modelo, costo) VALUES(?, ?, ?, ?, ?, ?)''',
        (id_maquinaria, nombre, estado, marca, modelo, costo)
    )

    conn.commit()
    conn.close()
    return c.rowcount


def consulta_componente(id_componente=''):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    if id_componente == '':
        c.execute('''SELECT * FROM componentes''')
    else:
        c.execute(
            '''SELECT * FROM componentes WHERE id= ?''', (id_componente,))
    res = c.fetchall()
    conn.commit()
    conn.close()
    return res


def consulta_historial_componente(id_componente=''):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    print(id_componente)
    c.execute(
        '''SELECT * FROM historial_componentes WHERE id_componente= ?''', (id_componente,))
    res = c.fetchall()
    conn.commit()
    conn.close()
    return res


def update_componente(
    id_componente,
    id_maquinaria,
    nombre,
    estado,
    marca,
    modelo,
    costo
):
    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()

    c.execute(
        '''UPDATE componentes
        SET id_maquinaria= ?,
            nombre= ?,
            estado= ?,
            marca= ?,
            modelo= ?,
            costo= ?
        WHERE id= ?''',
        (
            id_maquinaria,
            nombre,
            estado,
            marca,
            modelo,
            costo,
            id_componente
        )
    )

    conn.commit()
    conn.close()
    return c.rowcount


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def w_print(*text):
    print(bcolors.WARNING, *text, bcolors.ENDC)


def g_print(*text):
    print(bcolors.OKGREEN, *text, bcolors.ENDC)


def f_print(*text):
    print(bcolors.FAIL, *text, bcolors.ENDC)


def b_print(*text):
    print(bcolors.OKBLUE, *text, bcolors.ENDC)


def h_print(*text):
    print(bcolors.HEADER, *text, bcolors.ENDC)


def u_print(*text):
    print(bcolors.UNDERLINE, *text, bcolors.ENDC)


if __name__ == '__main__':
    remove_db()
    insert_user('admin@email.com', 'admin', 'admin',
                '12345678-9', 0)  # admin (type 0)
    insert_maquinaria('maquinaria1', 'nuevo', 100)
    insert_maquinaria('maquinaria2', 'casi nuevo', 200)
    insert_maquinaria('maquinaria3', 'usado', 50)
    insert_componente(1, 'componente2', 'nuevo', 'marca2', 'modelo2', 20)
    insert_componente(1, 'componente3', 'nuevo', 'marca3', 'modelo3', 30)
    insert_componente(2, 'componente4', 'nuevo', 'marca4', 'modelo4', 40)
    insert_componente(2, 'componente5', 'nuevo', 'marca5', 'modelo5', 50)
    insert_componente(2, 'componente6', 'nuevo', 'marca6', 'modelo6', 60)
    insert_componente(3, 'componente7', 'nuevo', 'marca7', 'modelo7', 70)
