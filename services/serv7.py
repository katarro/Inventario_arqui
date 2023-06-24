from utils import get_db_connection
import datetime
import socket
import psycopg2
import utils

def modificar_reserva(titulo ,nuevo_juego):
    try:
        conn = get_db_connection()
    except Exception as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return False
    
    try:
        c   = conn.cursor()
        if not titulo: raise ValueError("El título del juego reservado es necesario.")
        #Id del juego reservado
        c.execute('''SELECT idjuego, disponibilidad FROM juegos WHERE titulo = %s ''',(titulo,))
        conn.commit()
        idjuego = c.fetchone()

        if idjuego is not None:
            #Obtener id de la reserva
            c.execute('''SELECT idreserva FROM reservas WHERE idjuego = %s ''',(idjuego[0],))
            conn.commit()
            idreserva = c.fetchone()
            
            #Obtener id y disponibilida nuevo juego
            c.execute('''SELECT idjuego, disponibilidad FROM juegos WHERE titulo = %s ''',(nuevo_juego,))
            conn.commit()
            idnuevo_juego = c.fetchone()

            if idnuevo_juego is not None and idnuevo_juego[1]: 
                #Update de disponibilidad del juego reservado
                c.execute('''UPDATE juegos SET disponibilidad = False WHERE titulo = %s''', (nuevo_juego,) )
                conn.commit()
                #Update de disponibilidad del nuevo juego reservado
                c.execute('''UPDATE juegos SET disponibilidad = True WHERE titulo = %s''', (titulo,) )
                conn.commit()
                #Update de reserva
                c.execute('''UPDATE reservas SET idjuego=%s WHERE idreserva= %s''', (idnuevo_juego[0], idreserva[0]) )
                conn.commit()
                conn.close()
                return True
            else:
                conn.close()
                print(f"El juego {nuevo_juego} no existe o no se encuentra disponible en estos momentos.")
                return False
        else:
            conn.close()
            print(f"El juego {titulo} no existe.")
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

message = b"00100sinitserv7"

sock.send(message)
status = sock.recv(4096)[10:12].decode('UTF-8')
print(status)
if (status == 'OK'):
    print('Servicio Editar reserva iniciado de forma correcta\n')
    while True:
        received_message = sock.recv(4096).decode('UTF-8')
        print(received_message)
        client_id = received_message[5:10]
        data = eval(received_message[10:])
        ans = modificar_reserva(titulo=data['id'], nuevo_juego= data['nuevo_juego'])
        response = utils.str_bus_format(ans, str(client_id)).encode('UTF-8')
        sock.send(response)