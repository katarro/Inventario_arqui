import socket
import utils
import datetime
import psycopg2

def editar_horario(dia_semana, hora_apertura, hora_cierre, es_feriado):
    # dia_semana: (Lunes-Domingo)
    # hora_apertura: (00:00-23:59)
    # hora_cierre: (00:00-23:59)
    # es_feriado: (True/False)
    try:
        conn = utils.get_db_connection()
    except Exception as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return False     

    try:
        c = conn.cursor()
        # Obtener id del horario
        c.execute('''SELECT idhorario FROM horarios WHERE diasemana = %s''', (dia_semana,))
        conn.commit()
        id_horario = c.fetchone()

        if id_horario is not None:
            # Actualizar horario
            c.execute('''UPDATE horarios SET horaapertura = %s, horacierre = %s, esferiado = %s WHERE idhorario = %s''', (hora_apertura, hora_cierre, es_feriado))
            conn.commit()
            conn.close()
            return True
        else:
            conn.close()
            print(f"El horario del día {dia_semana} no existe.")
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

message = b"00100sinitserv9"

sock.send(message)
status = sock.recv(4096)[10:12].decode('UTF-8')
print(status)
if status == 'OK':
    print('Servicio editar horario iniciado de forma correcta\n')
    while True:
        received_message = sock.recv(4096).decode('UTF-8')
        print(received_message)
        client_id = received_message[5:10]
        data = eval(received_message[10:])
        # Llamar a la función crear_horario con los datos proporcionados
        exito = editar_horario(data['hora_apertura'], data['hora_cierre'], data['es_feriado'])
        if exito:
            response = utils.str_bus_format('Horario creado correctamente', str(client_id)).encode('UTF-8')
        else:
            response = utils.str_bus_format('Error al crear horario', str(client_id)).encode('UTF-8')
        sock.send(response)