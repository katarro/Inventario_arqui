import socket
import sys
import utils
import datetime
import psycopg2

def ver_horario(dia_semana):
    try:
        conn = utils.get_db_connection()
    except Exception as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return False
    
    try:
        c = conn.cursor()
        if dia_semana == '':
            c.execute('''SELECT diasemana, horaapertura, horacierre, esferiado FROM horarios ORDER BY idhorario''')
        else:
            c.execute('''SELECT diasemana, horaapertura, horacierre, esferiado FROM horarios WHERE diasemana = %s ORDER BY idhorario''', (dia_semana,))
        horario = c.fetchall()
        conn.commit()
        c.close()
        conn.close()
        return horario
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
message = b"00100sinitser10"
sock.send(message)

status = sock.recv(4096)[10:12].decode('UTF-8')
print(status)
if status == 'OK':
    print('Servicio mostrar horario iniciado de forma correcta\n')
    while True:
        received_message = sock.recv(4096).decode('UTF-8')
        print(received_message)
        client_id = received_message[5:10]
        data = eval(received_message[10:])
        ans = ver_horario(data['dia_semana'])
        response = utils.str_bus_format(ans, str(client_id)).encode('UTF-8')
        sock.send(response)
