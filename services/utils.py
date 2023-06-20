import psycopg2
import datetime
import hashlib
# from globals import id_user

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

def register(nombre, apellido, email, password, tipo_usuario):
    # validar codigo de ADMINISTRADOR
    if tipo_usuario == 'admin123':
        user_type = 'Administrador'
    else:
        user_type = 'Alumno'

    try:
        conn = get_db_connection()
    except Exception as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return False

    try:
        c = conn.cursor()

        # Verificar si los datos proporcionados son válidos
        if not all([nombre, apellido, email, password, user_type]):
            raise ValueError("Todos los campos son requeridos.")
        if "@" not in email:
            raise ValueError("Email inválido.")
        
        # Buscar el usuario en la base de datos
        c.execute(
            '''SELECT 1 FROM usuarios WHERE correo = %s ''',
            (email,)
        )
        conn.commit()
        user = c.fetchone()
        
        # Si no existe el usuario, hacer insert
        if user is None:
            c.execute(
                '''INSERT INTO usuarios (nombre, apellido, correo, contrasena, tipousuario) VALUES (%s, %s, %s, %s, %s)''',
                (nombre, apellido, email, password, user_type)
            )
            conn.commit()
            conn.close()
            return True
        else: 
            conn.close()
            return False

    except psycopg2.DatabaseError as e:
        print(f"Error en la consulta SQL: {e}")
        return False
    except ValueError as e:
        print(f"Error en los datos proporcionados: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False

def agregar_juego(titulo, descripcion, disponibilidad):
    # No permite agregar un juego si no esta disponible
    disponibilidad = disponibilidad.lower()
    if disponibilidad == 'si' or disponibilidad == 'true' or disponibilidad == 't':
        disponibilidad = True
    try:
        conn = get_db_connection()
    except Exception as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return False

    try:
        c = conn.cursor()

        # Verificar si los datos proporcionados son válidos
        if not all([titulo, descripcion, disponibilidad]):
            raise ValueError("Todos los campos son requeridos.")
        
        # Buscar el juego en la base de datos
        c.execute(
            '''SELECT 1 FROM juegos WHERE titulo = %s ''',
            (titulo,)
        )
        conn.commit()
        juego = c.fetchone()
        
        # Si no existe el juego, hacer insert
        if juego is None:
            c.execute(
                '''INSERT INTO juegos (titulo, descripcion, disponibilidad) VALUES (%s, %s, %s)''',
                (titulo, descripcion, disponibilidad)
            )
            conn.commit()
            conn.close()
            return True
        else: 
            conn.close()
            return False

    except psycopg2.DatabaseError as e:
        print(f"Error en la consulta SQL: {e}")
        return False
    except ValueError as e:
        print(f"Error en los datos proporcionados: {e}")
        return False
    except Exception as e:
        print(f"Error inesperado: {e}")
        return False




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








