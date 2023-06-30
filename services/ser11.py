import socket
import utils
import psycopg2

def editar_nombre_reserva(titulo, nombre_usuario):
    try:
        conn = utils.get_db_connection()
    except Exception as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return False
    
    #cambiar el id del usuario 
    try:
        c   = conn.cursor()
        if not titulo or not nombre_usuario: raise ValueError("El título del juego reservado o el nombre del usuario que reserbo el juego es necesario.")
        #Id del juego reservado
        c.execute('''SELECT idjuego, disponibilidad FROM juegos WHERE titulo = %s ''',(titulo,))
        conn.commit()
        idjuego = c.fetchone()

        if idjuego is not None:
            #Obtener id de la reserva
            c.execute('''SELECT idreserva FROM reservas WHERE idjuego = %s''',(idjuego[0],))
            conn.commit()
            idreserva = c.fetchone()
            
            #Update de reserva
            c.execute('''UPDATE reservas SET nombreusuario=%s WHERE idreserva= %s''', (nombre_usuario, idreserva[0]) )
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            print(f"El juego {titulo} no existe.")
            return False
    except Exception as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return False

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)
message = b"00100sinitser11"
sock.send(message)

status = sock.recv(4096)[10:12].decode('UTF-8')
print(status)
if status == 'OK':
    print('Servicio editar nombre de reserva de forma correcta\n')
    while True:
        received_message = sock.recv(4096).decode('UTF-8')
        print(received_message)
        client_id = received_message[5:10]
        data = eval(received_message[10:])
        ans = editar_nombre_reserva(titulo=data['id'], nombre_usuario= data['nombre_usuario'])
        response = utils.str_bus_format(ans, str(client_id)).encode('UTF-8')
        sock.send(response)
