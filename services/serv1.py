from utils import get_db_connection, sha1_hash
import socket
import utils 

def guardar_variable(nombre_archivo, variable):
    with open(nombre_archivo, 'w') as f:
        f.write(str(variable))


def login(correo, contrasena):
    print("Verificando usuario...")
    conn = get_db_connection()
    contrasena = sha1_hash(contrasena)
    cursor = conn.cursor()
    query = f"SELECT * FROM usuarios WHERE correo = '{correo}' AND contrasena = '{contrasena}';"
    cursor.execute(query)
    rows = cursor.fetchall()
    print(rows)
    conn.commit()
    cursor.close()
    conn.close()
    if len(rows) == 0:
        return None
    else:
        id_user = rows[0][0]
        guardar_variable("mi_variable.txt",id_user)
        return rows[0]



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('200.14.84.16', 5000)

sock.connect(server_address)

message = b"00050sinitserv1"
sock.send(message)
status = sock.recv(4096)[10:12].decode('UTF-8')
print("\n",status, end=" ")
if (status == 'OK'):
    print('Servicio login iniciado correctamente\n')
    while True:
        received_message = sock.recv(4096).decode('UTF-8')
        print(received_message)
        client_id = received_message[5:10]
        data = eval(received_message[10:])
        ans = login(data['email'], data['password'])
        response = utils.str_bus_format(ans, str(client_id)).encode('UTF-8')
        sock.send(response)
        
