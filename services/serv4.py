from utils import get_db_connection
import datetime
import psycopg2
import socket
import utils


def reservar_juego(titulo,nombre_usuario):

    try:
        conn = get_db_connection()
    except Exception as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return False
    
    try:
        c   = conn.cursor()
        if not titulo: raise ValueError("El título es requerido.")
        
        #Obtiene el id del usuario
        c.execute('''SELECT idusuario FROM usuarios WHERE nombre = %s ''',(nombre_usuario,))
        conn.commit()
        id_user = c.fetchone()

        # Obtiene el id del juego
        c.execute('''SELECT idjuego, disponibilidad FROM juegos WHERE titulo = %s ''',(titulo,))
        conn.commit()
        juego = c.fetchone()

        if juego is not None and juego[1]:
            c.execute('''UPDATE juegos SET disponibilidad = False WHERE titulo = %s''', (titulo,) )
            conn.commit()

            now = datetime.datetime.now()
            fechaReserva = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)

            c.execute('''INSERT INTO reservas (idusuario, idjuego, fechareserva, nombreusuario) VALUES (%s, %s, %s, %s)''', (id_user, juego[0], fechaReserva, nombre_usuario) )
            conn.commit()

            # Obtener el id de la reserva que acabamos de hacer
            c.execute('''SELECT idreserva FROM reservas WHERE idusuario = %s AND idjuego = %s AND fechareserva = %s''', (id_user, juego[0], fechaReserva))
            conn.commit()
            idreserva = c.fetchone()

            # Calcular la fecha de devolución (un día después de la fecha de reserva)
            fechaDevolucion = fechaReserva + datetime.timedelta(days=1)

            # Insertar la fecha de devolución en la tabla fechaDevolucion
            c.execute('''INSERT INTO fechas_devolucion (idreserva, fechadevolucion) VALUES (%s, %s)''', (idreserva[0], fechaDevolucion))
            conn.commit()
            print(conn.commit())

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
        nombre_usuario = data['nombre']

        ans = reservar_juego(titulo_juego,nombre_usuario)
        print('ans', ans)
        response = utils.str_bus_format(ans, str(client_id)).encode('UTF-8')
        sock.send(response)
