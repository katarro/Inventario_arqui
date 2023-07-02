from utils import get_db_connection
import socket
import utils

def view_catalog(titulo):

    conn = get_db_connection()
    cursor = conn.cursor()
    if titulo == '':
        pass
        query = "SELECT * FROM juegos;"
    else:
        #query = f"SELECT titulo, descripcion, disponibilidad FROM juegos WHERE titulo = '{titulo}';"
        query = f"SELECT * FROM juegos WHERE titulo = '{titulo}';"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return rows

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)
message = b"00050sinitserv3"
sock.send(message)

status = sock.recv(4096)[10:12].decode('UTF-8')
print(status, end=" ")
if (status == 'OK'):
    print('Servicio consulta juego iniciado correctamente\n')
    while True:
        received_message = sock.recv(4096).decode('UTF-8')
        print(received_message)
        client_id = received_message[5:10]
        data = eval(received_message[10:])
        ans = view_catalog(data['id'])
        response = utils.str_bus_format(ans, str(client_id)).encode('UTF-8')
        sock.send(response)
