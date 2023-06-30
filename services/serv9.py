from utils import get_db_connection
import socket
import utils
import datetime 

def leer_variable(nombre_archivo):
    with open(nombre_archivo, 'r') as f:
        variable = f.read()
    return int(variable) 

def gestion_fecha_prestamos( id_prestamo, nueva_fecha):
    id_user = leer_variable('mi_variable.txt')

    try:
        conn = get_db_connection()
    except Exception as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return False
    try:
        nueva_fecha = datetime.datetime.strptime(nueva_fecha, "%d/%m/%Y")
    except ValueError:
        print("Formato de fecha no válida, por favor ingresarla en el formato DD/MM/YYYY")
        return False
    try:
        c   = conn.cursor()
        if not id_prestamo or not nueva_fecha: raise ValueError("El título del juego reservado o/y la fecha nueva de reserva son necesarios.")
        #obtiene el prestamo
        c.execute('''SELECT id FROM reservas WHERE  id = %s ''',(id_prestamo,))
        conn.commit()
        prestamo = c.fetchone()

        if prestamo is not None: 
            #Obtener id de fechas prestamos
            c.execute('''SELECT id fecha FROM fechasPrestamos WHERE idreserva = %s ''',(prestamo[0]))
            conn.commit()
            fechas_prestamo = c.fetchone()

            if fechas_prestamo: 
                #Update de la fecha de prestamo
                c.execute('''UPDATE fechasPrestamos SET fechaprestamo = %s WHERE id = %s''', (fechas_prestamo[0],nueva_fecha) )
                conn.commit()
                conn.close()
                return True
            else:
                conn.close()
                print(f"No hay ninguna fecha asociada a la reserva {prestamo[0]}")
                return False
        else:
            conn.close()
            print(f"La reserva {prestamo[0]} no existe.")
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
if (status == 'OK'):
    print('Servicio gestion_fecha_prestamos iniciado de forma correcta\n')
    while True:
        received_message = sock.recv(4096).decode('UTF-8')
        print(received_message)
        client_id = received_message[5:10]
        data = eval(received_message[10:])
        ans = gestion_fecha_prestamos(
            id_prestamo=data['id_prestamo'],
            nueva_fecha=data['nueva_fecha']
        )
        response = utils.str_bus_format(ans, str(client_id)).encode('UTF-8')
        sock.send(response)
