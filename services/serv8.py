import socket
import utils
import psycopg2
from utils import get_db_connection

def leer_variable(nombre_archivo):
    with open(nombre_archivo, 'r') as f:
        variable = f.read()
    return int(variable) 

def eliminar_reserva(titulo):
    id_user = leer_variable('mi_variable.txt')

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
            c.execute('''SELECT idreserva FROM reservas WHERE idjuego = %s AND idUsuario = %s''',(idjuego[0], id_user))
            conn.commit()
            idreserva = c.fetchone()

            if idreserva is not None:    
                #Obtener id y disponibilida nuevo juego
                c.execute('''DELETE FROM reservas WHERE idreserva = %s ''',(idreserva[0],))
                conn.commit()
                #Actualizar disponibilidad del juego reservado
                c.execute('''UPDATE juegos SET disponibilidad = True WHERE titulo = %s''', (titulo,) )
                conn.commit()
            
                conn.close()
                return True
            else:
                conn.close()
                print(f"No tiene ninguna reserva del juego {titulo} actualmente.")
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

message = b"00100sinitserv8"

sock.send(message)
status = sock.recv(4096)[10:12].decode('UTF-8')
print(status)
if (status == 'OK'):
    print('Servicio eliminar reserva iniciado de forma correcta\n')
    while True:
        received_message = sock.recv(4096).decode('UTF-8')
        print(received_message)
        client_id = received_message[5:10]
        data = eval(received_message[10:])
        ans = eliminar_reserva(data['titulo'])
        response = utils.str_bus_format(ans, str(client_id)).encode('UTF-8')
        sock.send(response)
