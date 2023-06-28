import socket
import utils
import datetime
import psycopg2

def editar_horario(dia_semana, hora_apertura, hora_cierre, es_feriado=None):
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
        id_horario = c.fetchone()[0]

        campos_a_actualizar = []
        
        if hora_apertura:
            campos_a_actualizar.append(f"horaapertura = '{hora_apertura}'")
        if hora_cierre:
            campos_a_actualizar.append(f"horacierre = '{hora_cierre}'")
        if es_feriado is not None:
            
            if es_feriado == 'no' or es_feriado == 'No':
                es_feriado = False
                campos_a_actualizar.append(f"esferiado = {es_feriado}")

            if es_feriado == 'si' or es_feriado == 'Si':
                es_feriado = True
                campos_a_actualizar.append(f"esferiado = {es_feriado}")
        
        if not campos_a_actualizar:
            print("No se proporcionaron campos para actualizar.")
            return False
        
        consulta_sql = f"UPDATE horarios SET {', '.join(campos_a_actualizar)} WHERE idhorario = {id_horario};"
        print(consulta_sql)
        c.execute(consulta_sql)
        conn.commit()
        c.close()
        conn.close()
        return True
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