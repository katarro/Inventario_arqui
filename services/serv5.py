import psycopg2
import socket
import utils


def eliminar_juego(titulo):
    try:
        conn = utils.get_db_connection()
    except Exception as e:
        print(f"Error al conectarse a la base de datos: {e}")
        conn.close()
        return False

    try:
        c = conn.cursor()

        if not titulo: raise ValueError("El título es requerido.")
        
        c.execute('''SELECT idjuego FROM juegos WHERE titulo = %s ''', (titulo,) )
        conn.commit()
        juego = c.fetchone()
        
        if juego is not None:
            c.execute('''DELETE FROM juegos WHERE titulo = %s''', (titulo,) )
            conn.commit()

            print(f"Juego {titulo} eliminado correctamente.")
            conn.close()
            return True
        else: 
            conn.close()
            return False

    except psycopg2.DatabaseError as e:
        print(f"Error en la consulta SQL: {e}")
        conn.close()
        return False
    
    except ValueError as e:
        print(f"Error en los datos proporcionados: {e}")
        conn.close()
        return False
    
    except Exception as e:
        print(f"Error inesperado: {e}")
        conn.close()
        return False


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)
message = b"00050sinitserv5"
sock.send(message)
status = sock.recv(4096)[10:12].decode('UTF-8')
print(status)
if (status == 'OK'):
    print('Servicio eliminar juego iniciado exitosamente\n')
    while True:
        received_message = sock.recv(4096).decode('UTF-8')
        print(received_message)
        client_id = received_message[5:10]
        data = eval(received_message[10:])
        ans = eliminar_juego(data['id'])
        response = utils.str_bus_format(ans, str(client_id)).encode('UTF-8')
        sock.send(response)
