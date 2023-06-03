import socket
from services.utils import str_bus_format, w_print, f_print, g_print, h_print, b_print, bcolors
# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address = ('localhost', 5000)
# sock.connect(server_address)


class App:
    def __init__(self, register_service, login_service, services=[]) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', 5000)
        self.sock.connect(server_address)
        self.services = services
        self.login_service = login_service
        self.register_service = register_service

    def send_message(self, data, service_name='g7999'):
        req = str_bus_format(data, service_name).encode('UTF-8')
        self.sock.send(req)
        return self.sock.recv(4096).decode('UTF-8')

    def register(self):
        h_print('\n', '-'*20, 'Register', '-'*20, '\n')
        inputs = {}
        for i in range(len(self.register_service['inputs'])):
            actual_input = self.register_service['inputs'][i]
            key = actual_input['key']
            inputs[key] = input(actual_input['desc'])
        res = self.send_message(inputs, self.register_service['id'])
        return res

    def login(self):
        h_print('\n', '-'*20, 'Login', '-'*20, '\n')
        inputs = {}
        for i in range(len(self.login_service['inputs'])):
            actual_input = self.login_service['inputs'][i]
            key = actual_input['key']
            inputs[key] = input(actual_input['desc'])
        res = self.send_message(inputs, self.login_service['id'])
        return res

    def show_menu(self):
        while True:
            h_print("\n", "-"*20, "Bienvenido", "-"*20, "\n")
            b_print("Menu de opciones:\n")
            print("Opcion 1: {}".format(self.register_service['desc']))
            print("Opcion 2: {}".format(self.login_service['desc']))
            print("Opcion 0: Salir")
            option = input('Ingrese una opcion: ')

            if option == '1':
                res = self.register()
                data = eval(res[12:])
                if res[10:12] == 'NK':
                    f_print('Servicio no disponible')
                    pass
                elif data == False:
                    f_print('Registro fallido, Complete todos los campos o use un usuario que no este registrado')
                    pass
                else:
                    g_print('Registro exitoso')
                    pass

            elif option == '2':
                res = self.login()
                data = eval(res[12:])
                if res[10:12] == 'NK':
                    f_print('Servicio no disponible')
                    pass
                elif data == None:
                    f_print('Login fallido')
                    pass
                else:
                    g_print('Login exitoso')
                    self.menu(data[-1])

            elif option == '0':
                return
            else:
                w_print("Opcion no valida")


    def menu(self, type_id):
        while True:
            input(
                f'{bcolors.UNDERLINE}Presione enter para continuar...{bcolors.ENDC}')
            h_print("\n", "-"*20, "Bienvenido", "-"*20, "\n")
            b_print("Menu de opciones:\n")
            available_services = [
                service for service in self.services
            ]
            services = {}
            for i in range(len(available_services)):
                actual_service = available_services[i]
                services[f'{i+1}'] = actual_service
                print("Opcion {}: {}".format(i+1, actual_service['desc']))
            print("Opcion 0: Salir")
            option = input('Ingrese una opcion: ')
            if option == '0':
                return
            elif option in services:
                service = services[option]
                inputs = {}
                for i in range(len(service['inputs'])):
                    actual_input = service['inputs'][i]
                    key = actual_input['key']
                    inputs[key] = input(actual_input['desc'])
                res = self.send_message(inputs, service['id'])
                if res[10:12] == 'NK':
                    f_print('Servicio no disponible')
                    pass
                else:
                    service['function'](res)
            else:
                w_print("Opcion no valida")


def display_juegos(res):
    data = eval(res[12:])
    juegos = [juego for juego in data if juego[1]]
    
    if len(juegos) == 0:
        f_print('No se encontraron juegos')
        return
    
    columnas = ['titulo', 'descripcion', 'disponibilidad']
    
    g_print('Juegos encontrados:')
    
    for juego in juegos:
        b_print('-' * 20)
        for columna in columnas:
            indice = columnas.index(columna) + 1
            valor = juego[indice]
            if columna == 'disponibilidad':
                if valor:
                    valor = '\033[92m' + 'Disponible' + '\033[0m'  # Color verde
                else:
                    valor = '\033[91m' + 'No disponible' + '\033[0m'  # Color rojo
            print(f'{columna.capitalize()}: {valor}')
        print()



def display_componentes(res):
    data = eval(res[12:])
    componentes = [componente for componente in data if not componente[8]]
    if len(data) == 0:
        f_print('No se encontraron componentes')
        return
    g_print('Componentes encontrados:')
    for componente in componentes:
        b_print('-'*20)
        print('id', componente[0])
        print('id_maquinaria', componente[1])
        print('nombre', componente[2])
        print('estado', componente[3])
        print('marca', componente[4])
        print('modelo', componente[5])
        print('costo', componente[6])
        print('fecha de creacion', componente[7])


def display_historial_componente(res):
    data = eval(res[12:])
    for componente in data:
        b_print('-'*20)
        print('id', componente[0])
        print('id_maquinaria', componente[1])
        print('nombre', componente[2])
        print('estado', componente[3])
        print('marca', componente[4])
        print('modelo', componente[5])
        print('costo', componente[6])
        print('fecha de modificacion', componente[7])


if __name__ == '__main__':
    app = App(
        register_service={
            'id': 'serv0',
            'desc': 'Registrarse',
            'inputs': [
                {
                    'key': 'nombre',
                    'desc': 'Ingresa tu nombre: '
                },
                {
                    'key': 'apellido',
                    'desc': 'Ingresa tu apellido: '
                },
                {
                    'key': 'email',
                    'desc': 'Ingresa tu email: '
                },
                {
                    'key': 'password',
                    'desc': 'Ingresa tu contraseña: '
                },
                {
                    'key': 'tipo_usuario',
                    'desc': 'Ingresa que tipo de usuario eres: '
                },
            ]
        },
        login_service={
            'id': 'serv1',
            'desc': 'Iniciar sesión',
            'inputs': [
                {
                    'key': 'email',
                    'desc': 'Ingresa tu mail: '
                },
                {
                    'key': 'password',
                    'desc': 'Ingresa tu contraseña: '
                }
            ]
        },
        services=[           
            {
                'id': 'serv3',
                'desc': 'Consultar juegos de mesa',
                'user_types': [0, 1, 2],
                'function': display_juegos,
                'inputs': [
                    {
                        'key': 'id',
                        'desc': 'Nombre del juego o vacío para consultar por todos: '
                    }
                ]
            },
        ]
    )
    res = app.show_menu()
