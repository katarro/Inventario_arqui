from utils import agregar_juego
import socket
import utils


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5000)
sock.connect(server_address)
message = b"00050sinitserv2"



sock.send(message)
status = sock.recv(4096)[10:12].decode('UTF-8')
print("\n",status, end=" ")
if (status == 'OK'):
    print('Servicio agregar nuevo juego iniciado correctamente\n')
    while True:
        received_message = sock.recv(4096).decode('UTF-8')
        print(received_message)
        client_id = received_message[5:10]
        data = eval(received_message[10:])
        
        ans = agregar_juego(data['titulo'], data['descripcion'], data['disponibilidad'])

        response = utils.str_bus_format(ans, str(client_id)).encode('UTF-8')
        sock.send(response)
