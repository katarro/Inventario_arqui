import psycopg2
from utils import get_db_connection
import socket
import utils
import datetime 

def leer_variable(nombre_archivo):
    with open(nombre_archivo, 'r') as f:
        variable = f.read()
    return int(variable) 

def gestion_fecha_prestamos( nombre_juego, nueva_fecha):
    id_user = leer_variable('mi_variable.txt')

    try:
        conn = get_db_connection()
    except Exception as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return False
    try:
        nueva_fecha = datetime.datetime.strptime(nueva_fecha, "%Y-%m-%d").date()
    except ValueError:
        print("Formato de fecha no válida, por favor ingresarla en el formato DD-MM-YYYY")
        return False
    try:
        #return nueva_fecha
        c   = conn.cursor()
        if not nombre_juego or not nueva_fecha: raise ValueError("El título del juego reservado o/y la fecha nueva de reserva son necesarios.")
        #obtiene el ID del juego
        c.execute('''SELECT id FROM juegos WHERE titulo = %s ''',(nombre_juego))
        conn.commit()
        juego = c.fetchone()

        if juego is not None: 
            #Obtener id del prestamo
            c.execute('''SELECT id FROM reservas WHERE id = %s ''',(juego[0]))
            conn.commit()
            prestamo = c.fetchone()
            if prestamo: 
                #Update de la fecha de prestamo
                c.execute('''INSERT INTO fechasPrestamos (idreserva, fechaprestamo) VALUES( %s, %s)''',(prestamo[0],nueva_fecha))
                conn.commit()
                conn.close()
                return True
            else:
                conn.close()
                print(f"No hay ninguna fecha asociada a la reserva del juego{nombre_juego}")
                return False
        else:
            conn.close()
            print(f"el juego {nombre_juego} no existe.")
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

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)

sock.connect(server_address)

message = b"00100sinitserv9"


sock.send(message)
status = sock.recv(4096)[10:12].decode('UTF-8')
print(status)
if (status == 'OK'):
    print('Servicio gestion_fecha_prestamos iniciado de forma correcta\n')
    while True:
        received_message = sock.recv(4096).decode('UTF-8')
        print(received_message)
        client_id = received_message[5:10]
        data = eval(received_message[10:])
        ans = gestion_fecha_prestamos(
            nombre_juego=data['nombre_juego'],
            nueva_fecha=data['nueva_fecha']
        )
        response = utils.str_bus_format(ans, str(client_id)).encode('UTF-8')
        sock.send(response)