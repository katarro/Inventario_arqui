import socket
import psycopg2
import utils
import datetime
from utils import get_db_connection

def agregar_multa(nombre, apellido):
    try:
        conn = get_db_connection()
    except Exception as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return False
    
    try:
        c   = conn.cursor()
        if not nombre or not apellido: raise ValueError("Porfavor especifique un nombre y apellido de alumno.")
        #Id del alumno
        c.execute('''SELECT idusuario FROM usuarios WHERE nombre = %s AND apellido =%s''',(nombre,apellido))
        conn.commit()
        idusuario = c.fetchone()

        if idusuario is not None:
            now = datetime.datetime.now()
            fechamulta = datetime.datetime(now.year, now.month, now.day, now.hour, now.minute, now.second)
            
            #crear multa
            c.execute('''INSERT INTO multas (idusuario, fechamulta, baneotemporal) VALUES( %s, %s, %s)''',(idusuario[0], fechamulta, True,))
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

message = b"00100sinitserv10"

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
        ans = agregar_multa(nombre=data['nombre'], apellido=data['apellido'])
        response = utils.str_bus_format(ans, str(client_id)).encode('UTF-8')
        sock.send(response)

