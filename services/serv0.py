from utils import insert_user, sha1_hash
import socket
import utils


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('200.14.84.16', 5000)

sock.connect(server_address)

message = b"00050sinitserv0"

sock.send(message)
status = sock.recv(4096)[10:12].decode('UTF-8')
print("\n",status, end=" ")
if (status == 'OK'):
    print('Servicio registro_usuario iniciado correctamente\n')
    while True:
        received_message = sock.recv(4096).decode('UTF-8')
        client_id = received_message[5:10]
        data = eval(received_message[10:])

        #si hay un valor nulo
        if any(value is None for value in data.values()):
            response = False
        
        #Si no hay valores nulos
        else:
            ans = insert_user(
                nombre       = data['nombre'],
                apellido     = data['apellido'],
                email        = data['email'],
                password     = sha1_hash(data['password']),
                tipo_usuario = data['tipo_usuario'],
            )
            response = utils.str_bus_format(ans, str(client_id)).encode('UTF-8')
        sock.send(response)
