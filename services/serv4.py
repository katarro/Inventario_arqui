from utils import get_db_connection
import datetime
import psycopg2
import socket
import utils

def leer_variable(nombre_archivo):
    with open(nombre_archivo, 'r') as f:
        variable = f.read()
    return int(variable) 

def reservar_juego(titulo):
    id_user = leer_variable('mi_variable.txt')

    try:
        conn = get_db_connection()
    except Exception as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return False
    
    try:
        c   = conn.cursor()
        if not titulo: raise ValueError("El título es requerido.")
        
        #Obtiene el nombre del usuario por su id
        c.execute('''SELECT nombre FROM usuarios WHERE idusuario = %s ''',(id_user,))
        conn.commit()
        nombre = c.fetchone()

        c.execute('''SELECT idjuego, disponibilidad FROM juegos WHERE titulo = %s ''',(titulo,))
        conn.commit()
        juego = c.fetchone()

        if juego is not None and juego[1]:
            c.execute('''UPDATE juegos SET disponibilidad = False WHERE titulo = %s''', (titulo,) )
            conn.commit()

            now = datetime.datetime.now()
            fechaReserva = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)

            c.execute('''INSERT INTO reservas (idusuario, idjuego, fechareserva, nombreusuario) VALUES (%s, %s, %s, %s)''', (id_user, juego[0], fechaReserva, nombre[0]) )
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





sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)
message = b"00050sinitserv4"

sock.send(message)
status = sock.recv(4096)[10:12].decode('UTF-8')
print("\n",status,end=" ")
if (status == 'OK'):
    print('Servicio Reserva de juego iniciado correctamente\n')
    while True:
        received_message = sock.recv(4096).decode('UTF-8')
        print(received_message)
        client_id = received_message[5:10]
        data = eval(received_message[10:])
        titulo_juego = data['id']

        ans = reservar_juego(titulo_juego)
        print('ans', ans)
        response = utils.str_bus_format(ans, str(client_id)).encode('UTF-8')
        sock.send(response)
