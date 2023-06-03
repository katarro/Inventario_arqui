import socket
import utils
import psycopg2
from utils import consulta_maquinaria

def view_catalog(nombre):
    print(nombre)
    conn = psycopg2.connect(
        host="bbpzwcbmdyu2wotib6og-postgresql.services.clever-cloud.com",
        port="5432",
        dbname="bbpzwcbmdyu2wotib6og",
        user="uwnuqyetyjpariikmobj",
        password="Is7jUIMZs9x9QLc93kd6WuHIw85Et4"
    )
    cursor = conn.cursor()
    query = f"SELECT * FROM juegos;"
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return rows

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('200.14.84.16', 5000)

sock.connect(server_address)

message = b"00050sinitserv3"

sock.send(message)
status = sock.recv(4096)[10:12].decode('UTF-8')
print(status)
if (status == 'OK'):
    print('Servicio consulta juego iniciado de forma correcta\n')
    while True:
        received_message = sock.recv(4096).decode('UTF-8')
        print(received_message)
        client_id = received_message[5:10]
        data = eval(received_message[10:])
        ans = view_catalog()
        response = utils.str_bus_format(ans, str(client_id)).encode('UTF-8')
        sock.send(response)
