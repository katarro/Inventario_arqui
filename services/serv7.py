from utils import get_db_connection
import socket
import psycopg2
import utils

def leer_variable(nombre_archivo):
    with open(nombre_archivo, 'r') as f:
        variable = f.read()
    return int(variable) 

def modificar_reserva(juego_actual ,nuevo_juego):
    id_user = leer_variable('mi_variable.txt')
    # aqui, hacer consulta sql para obtener el id del usuario

    # El usuario debe cambiar de juego

    # 1. Verificar que exitan los juegos 
    # 2. Verificar que nuevo juego este disponible
    # 3. Hacer el cambio




    try:
        conn = get_db_connection()
    except Exception as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return False
    
    try:
        c   = conn.cursor()
        if not juego_actual or not nuevo_juego: raise ValueError("El título del juego reservado o el juego a reservar es necesario.")
        
        #Id del juego actual
        c.execute('''SELECT idjuego, disponibilidad FROM juegos WHERE titulo = %s ''',(juego_actual,))
        conn.commit()
        idjuego_actual = c.fetchone()

        if idjuego_actual is not None:
            
            #Obtener id de la reserva
            c.execute('''SELECT idreserva FROM reservas WHERE idjuego = %s AND idusuario = %s''',(idjuego_actual[0],id_user))
            conn.commit()
            idreserva = c.fetchone()
            
            #Obtener id y disponibilida nuevo juego
            c.execute('''SELECT idjuego, disponibilidad FROM juegos WHERE juego_actual = %s ''',(nuevo_juego,))
            conn.commit()
            idnuevo_juego = c.fetchone()

            if idnuevo_juego is not None and idnuevo_juego[1]: 
                #Update de disponibilidad del juego reservado
                c.execute('''UPDATE juegos SET disponibilidad = False WHERE juego_actual = %s''', (nuevo_juego,) )
                conn.commit()
                #Update de disponibilidad del nuevo juego reservado
                c.execute('''UPDATE juegos SET disponibilidad = True WHERE juego_actual = %s''', (juego_actual,) )
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
            print(f"El juego {juego_actual} no existe.")
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
        ans = modificar_reserva(juego_actual=data['id'], nuevo_juego= data['nuevo_juego'])
        response = utils.str_bus_format(ans, str(client_id)).encode('UTF-8')
        sock.send(response)