import socket
import utils
import datetime
import psycopg2

def ver_horario(diasemana):
    try:
        conn = utils.get_db_connection()
    except Exception as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return False
    
    try:
        cursor = conn.cursor()
        if diasemana == '':
            pass
            query = "SELECT * FROM horario;"
        else:
            query = f"SELECT * FROM horario WHERE diasemana = '{diasemana}';"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return rows
    

        
    
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
if status == 'OK':
    print('Servicio ver horario iniciado de forma correcta\n')
    while True:
        received_message = sock.recv(4096).decode('UTF-8')
        print(received_message)
        client_id = received_message[5:10]
        data = eval(received_message[10:])
        ans = ver_horario()
        response = utils.str_bus_format(ans, str(client_id)).encode('UTF-8')
        sock.send(response)
        print(response)
        print('Respuesta enviada\n')
        break
else:
    print('Error al iniciar el servicio\n')
    sock.close()
    exit(1)
    