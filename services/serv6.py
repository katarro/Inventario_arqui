import socket
import utils



def editar_juego(titulo, nuevo_titulo='', nueva_descripcion='', nueva_disponibilidad=None):
    try:
        conn = utils.get_db_connection()
    except Exception as e:
        print(f"Error al conectarse a la base de datos: {e}")
        return False

    try:
        c = conn.cursor()
        c.execute('''SELECT * FROM reservas WHERE idjuego = (SELECT idjuego FROM juegos WHERE titulo = %s)''', (titulo,) )
        reservas = c.fetchall()
        
        if reservas:
            print(f"No se puede editar el juego '{titulo}' porque está reservado (ver tabla reservas).")
            conn.close()
            return False

        campos_a_actualizar = []
        if nuevo_titulo:
            campos_a_actualizar.append(f"titulo = '{nuevo_titulo}'")
        if nueva_descripcion:
            campos_a_actualizar.append(f"descripcion = '{nueva_descripcion}'")
        if nueva_disponibilidad is not None:
            
            if nueva_disponibilidad == 'no' or nueva_disponibilidad == 'No':
                nueva_disponibilidad = False
                campos_a_actualizar.append(f"disponibilidad = {nueva_disponibilidad}")
            
            if nueva_disponibilidad == 'si' or nueva_disponibilidad == 'Si':
                nueva_disponibilidad = True
                campos_a_actualizar.append(f"disponibilidad = {nueva_disponibilidad}")
            
        
        if not campos_a_actualizar:
            print("No se proporcionaron campos para actualizar.")
            return False

        consulta_sql = f"UPDATE juegos SET {', '.join(campos_a_actualizar)} WHERE titulo = '{titulo}';"
        
        c.execute(consulta_sql)
        conn.commit()
        conn.close()

        return True
    except Exception as e:
        print(f"Error al actualizar el juego: {e}")
        return False
    finally:
        c.close()
        conn.close()



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)
message = b"00050sinitserv6"
sock.send(message)
status = sock.recv(4096)[10:12].decode('UTF-8')
print(status)
if (status == 'OK'):
    print('Servicio editar juego iniciado correctamente\n')
    while True:
        received_message = sock.recv(4096).decode('UTF-8')
        print(received_message)
        client_id = received_message[5:10]
        data = eval(received_message[10:])
        print("DATA: ",data)
        ans = editar_juego(data['id'],data['nuevo_titulo'], data['nueva_descripcion'], data['nueva_disponibilidad'])
        response = utils.str_bus_format(ans, str(client_id)).encode('UTF-8')
        sock.send(response)
