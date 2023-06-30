import socket
import psycopg2
import utils
import datetime
from utils import get_db_connection

def agregar_multa():
    try:
        conn = get_db_connection()
    except Exception as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return False
    
    try:
        c   = conn.cursor()
        #Chequear todas las fechas
        c.execute('''SELECT idusuario FROM reservas WHERE fechareserva > CURRENT_DATE;''')
        conn.commit()
        idreservas = c.fetchall()
        print(idreservas)
        
        if idreservas is not None:
            #crear multa
            c.execute('''SELECT nombre , apellido FROM usuarios WHERE idusuario IN (SELECT UNNEST(%s))''',(idreservas,))
            conn.commit()
            usuarios = c.fetchall()
            print(usuarios)
            conn.close()
            return usuarios
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

message = b"00100sinitser14"

sock.send(message)
status = sock.recv(4096)[10:12].decode('UTF-8')
print(status)
if (status == 'OK'):
    print('Servicio de multas iniciado de forma correcta\n')
    while True:
        received_message = sock.recv(4096).decode('UTF-8')
        print(received_message)
        client_id = received_message[5:10]
        data = eval(received_message[10:])
        ans = agregar_multa(data['id'])
        response = utils.str_bus_format( ans,str(client_id)).encode('UTF-8')
        sock.send(response)


