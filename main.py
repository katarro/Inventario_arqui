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


def display_maquinarias(res):   #IMPORTANTEEEE
    data = eval(res[12:])
    maquinarias = [maquinaria for maquinaria in data if maquinaria[1]]
    if len(maquinarias) == 0:
        f_print('No se encontraron maquinarias')
        return
    g_print('Maquinarias encontradas:')
    for maquinaria in maquinarias:
        b_print('-'*20)
        print('id', maquinaria[0])
        print('nombre', maquinaria[1])
        print('descripcion', maquinaria[2])
        print('disponibilidad', maquinaria[3])


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
                'id': 'serv2',
                'desc': 'Registrar maquinaria',
                'user_types': [0, 1, 2],
                'function': lambda *_: g_print('maquinaria registrada'),
                'inputs': [
                    {
                        'key': 'nombre',
                        'desc': 'Ingresa el nombre de la maquinaria: ',
                    },
                    {
                        'key': 'estado',
                        'desc': 'Ingresa el estado de la maquinaria: ',
                    },
                    {
                        'key': 'costo',
                        'desc': 'Ingresa el costo de la maquinaria: '
                    }
                ]
            },
            {
                'id': 'serv3',
                'desc': 'Consultar juegos de mesa',
                'user_types': [0, 1, 2],
                'function': display_maquinarias,
                'inputs': [
                    {
                        'key': 'id',
                        'desc': 'Ingresa el id del juego de mesa o vacío para consultar por todos: '
                    }
                ]
            },
            {
                'id': 'serv4',
                'desc': 'Modificar maquinaria',
                'user_types': [0, 1, 2],
                'function': lambda res: g_print('maquinaria modificada') if eval(res[12:]) > 0 else f_print('maquinaria no encontrada'),
                'inputs': [
                    {
                        'key': 'id',
                        'desc': 'Ingresa el id de la maquinaria: '
                    },
                    {
                        'key': 'nombre',
                        'desc': 'Ingresa el nuevo nombre de la maquinaria: ',
                    },
                    {
                        'key': 'estado',
                        'desc': 'Ingresa el nuevo estado de la maquinaria: ',
                    },
                    {
                        'key': 'costo',
                        'desc': 'Ingresa el nuevo costo de la maquinaria: '
                    }
                ]
            },
            {
                'id': 'serv5',
                'desc': 'Eliminar maquinaria',
                'user_types': [0, 1, 2],
                'function': lambda res: g_print('maquinaria eliminada') if eval(res[12:]) > 0 else f_print('maquinaria no encontrada'),
                'inputs': [
                    {
                        'key': 'id',
                        'desc': 'Ingresa el id de la maquinaria: '
                    }
                ]
            },
            {
                'id': 'serv6',
                'desc': 'Registrar componente',
                'user_types': [0, 1, 2],
                'function': lambda *_: g_print('componente registrado'),
                'inputs': [
                    {
                        'key': 'nombre',
                        'desc': 'Ingresa el nombre del componente: ',
                    },
                    {
                        'key': 'estado',
                        'desc': 'Ingresa el estado del componente: ',
                    },
                    {
                        'key': 'marca',
                        'desc': 'Ingresa la marca del componente: '
                    },
                    {
                        'key': 'modelo',
                        'desc': 'Ingresa el modelo del componente: '
                    },
                    {
                        'key': 'costo',
                        'desc': 'Ingresa el costo del componente: '
                    },
                    {
                        'key': 'id_maquinaria',
                        'desc': 'Ingresa el id de la maquinaria: '
                    },
                ]
            },
            {
                'id': 'serv7',
                'desc': 'Consultar componentes',
                'user_types': [0, 1, 2],
                'function': display_componentes,
                'inputs': [
                    {
                        'key': 'id',
                        'desc': 'Ingresa el id del componente o vacío para consultar por todas: '
                    }
                ]
            },
            {
                'id': 'serv8',
                'desc': 'Modificar componente',
                'user_types': [0, 1, 2],
                'function': lambda res: g_print('componente modificado') if (eval(res[12:])) > 0 else f_print('componente no encontrado'),
                'inputs': [
                    {
                        'key': 'id',
                        'desc': 'Ingresa el id del componente: '
                    },
                    {
                        'key': 'nombre',
                        'desc': 'Ingresa el nuevo nombre del componente: ',
                    },
                    {
                        'key': 'estado',
                        'desc': 'Ingresa el nuevo estado del componente: ',

                    },
                    {
                        'key': 'marca',
                        'desc': 'Ingresa la nueva marca del componente: '
                    },
                    {
                        'key': 'modelo',
                        'desc': 'Ingresa el nuevo modelo del componente: '
                    },
                    {
                        'key': 'costo',
                        'desc': 'Ingresa el nuevo costo del componente: '
                    },
                    {
                        'key': 'id_maquinaria',
                        'desc': 'Ingresa el nuevo id de la maquinaria: '
                    },
                ]
            },
            {
                'id': 'serv9',
                'desc': 'Historial de componente',
                'user_types': [0, 1, 2],
                'function': display_historial_componente,
                'inputs': [
                    {
                        'key': 'id',
                        'desc': 'Ingresa el id del componente: '
                    }
                ]
            }
        ]
    )
    res = app.show_menu()
