import socket
import utils
import datetime
import psycopg2
import re

def validar(tiempo):
    patron = r'^([01]\d|2[0-3]):([0-5]\d)$'
    coincidencia = re.match(patron, tiempo)
    if coincidencia:
        return True
    else:
        return False

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
        dia=str(dia_semana).lower()
        print(dia_semana)
        c = conn.cursor()
        # Obtener id del horario
        horario = c.execute('''SELECT idhorario FROM horarios WHERE diasemana = %s''', (dia))
        if horario:
            id_horario = horario[0]
            campos_a_actualizar = []
            if hora_apertura and validar(hora_apertura):
                campos_a_actualizar.append(f"horaapertura = '{hora_apertura}'")
            else:
                print("debe proporcionar una hora en formato HH:MM")
            if hora_cierre and validar(hora_cierre):
                campos_a_actualizar.append(f"horacierre = '{hora_cierre}'")
            else:
                print("debe proporcionar una hora en formato HH:MM")
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
        else:
            print("se debe proporcionar un día de la semana en el siguiente formato: lunes, martes, miercoles, jueves, viernes, sabado, domingo")
        
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
message = b"00100sinitser12"
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
        print("DATA: ",data)
        exito = editar_horario(data['dia_semana'], data['hora_apertura'], data['hora_cierre'], data['es_feriado'])
        response = utils.str_bus_format(exito, str(client_id)).encode('UTF-8')
        sock.send(response)