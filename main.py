from services.utils import str_bus_format, w_print, f_print, g_print, h_print, b_print, bcolors
import readline
import socket
import re
import os
import getpass
import datetime

# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server_address = ('localhost', 5000)
# sock.connect(server_address)

readline.set_history_length(100)  # Número máximo de comandos a recordar

class App:
    def __init__(self, register_service, login_service, services=[], admin_services=[]) -> None:
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.register_service = register_service
        self.admin_services = admin_services
        server_address = ('localhost', 5000)
        self.login_service = login_service
        self.sock.connect(server_address)
        self.services = services

    def send_message(self, data, service_name='g7999'):
        req = str_bus_format(data, service_name).encode('UTF-8')
        self.sock.send(req)
        return self.sock.recv(4096).decode('UTF-8')

    def register(self):
        os.system('clear')
        h_print('\n', '-'*20, 'Register', '-'*20, '\n')
        inputs = {}
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        for i in range(len(self.register_service['inputs'])):
            actual_input = self.register_service['inputs'][i]
            key = actual_input['key']
            desc = actual_input['desc']
            value = input(desc)

            while not value.strip(): 
                print("El valor no puede estar vacío.")
                value = input(desc)

            if key == 'email':
                while not re.match(email_pattern, value):
                    print("El correo electrónico ingresado no es válido.")
                    value = input(desc)

            inputs[key] = value

        res = self.send_message(inputs, self.register_service['id'])
        return res

    def login(self):
        h_print('\n', '-'*20, 'Login', '-'*20, '\n')
        inputs = {}
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

        for i in range(len(self.login_service['inputs'])):
            actual_input = self.login_service['inputs'][i]
            key = actual_input['key']
            desc = actual_input['desc']
            if key == 'password':
                value = getpass.getpass(desc)
            else:
                value = input(desc)

            while not value.strip():  # Verificar si el string está vacío o contiene solo espacios en blanco
                print("El valor no puede estar vacío.")
                value = getpass.getpass(desc)

            if key == 'email':
                while not re.match(email_pattern, value):
                    print("El correo electrónico ingresado no es válido.")
                    value = input(desc)

            inputs[key] = value

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

                elif data == None:
                    f_print('Login fallido')

                else:
                    os.system('clear')
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
            
            # Decide qué servicios mostrar basado en el tipo de usuario
            if type_id == 'Administrador':
                available_services = self.admin_services
                os.system('clear')
                g_print("Menu de administrador:\n")

            else:
                available_services = self.services
                os.system('clear')
                g_print("Menu de usuario:\n")
                
            services = {}
            for i in range(len(available_services)):
                actual_service = available_services[i]
                services[f'{i+1}'] = actual_service
                print("Opcion {}: {}".format(i+1, actual_service['desc']))
            print("Opcion 0: Salir")
            option = input('Ingrese una opcion: ')
            if option == '0':
                os.system('clear')
                return
            elif option in services:
                service = services[option]
                inputs = {}
                for i in range(len(service['inputs'])):
                    actual_input = service['inputs'][i]
                    key = actual_input['key']
                    inputs[key] = input(actual_input['desc'])
                res = self.send_message(inputs, service['id']) # Dirige al servicio correspondiente
                print(res,res[10:12])
                if res[10:12] == 'NK':
                    f_print('Servicio no disponible')
                    pass
                else:
                    print(res,"\n")
                    service['function'](res)
            else:
                w_print("Opcion no valida")

def display_juegos(res):
    os.system('clear')
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

#imprime el horario
def display_horario(res):
    os.system('clear')
    data = eval(res[12:])
    columnas = ['dia_semana', 'hora_apertura', 'hora_cierre', 'esferiado']
    g_print('Horario:')
    for horario in data:
        b_print('-' * 20)
        for columna in columnas:
            indice = columnas.index(columna)
            valor = horario[indice]
            if columna == 'esferiado':
                if valor:
                    valor = '\033[91m' + 'Es feriado' + '\033[0m'
                else:
                    valor = '\033[92m' + 'No es feriado' + '\033[0m'
            print(f'{columna.capitalize()}: {valor}')
        print()

def display_multas(res):
    os.system('clear')
    data = eval(res[12:])
    usuarios = [usuario for usuario in data]
    
    if len(usuarios) == 0:
        f_print('No se encontraron multas')
        return
    
    columnas = ['nombre', 'apellido']
    
    g_print('Multas:')
    
    for usuario in usuarios:
        #b_print('-' * 20)
        for i in usuario:
            print(i,' ')
        print('\n')

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
                    'desc': 'Ingresa tipo de usuario [admin] [alumno]:  '
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
            {
                'id': 'serv4',
                'desc': 'Reservar juego',
                'function' : lambda res: g_print('Juego Rervado exitosamente') if eval(res[12:]) else f_print('No se pudo Rservar el juego :( '),
                'inputs':[
                    {
                        'key': 'id',
                        'desc': 'Nombre del juego que desea Reservar: '
                    }
                ]
            },
            {
                'id':'serv7',
                'desc': 'Modificar Reserva',
                'function': lambda res: g_print('Reserva editada exitosamente') if eval(res[12:]) else f_print('No se pudo editar la reserva'),
                'inputs':[                    
                    {
                        'key':'id',
                        'desc':'Nombre del juego que reservo: '
                    },
                    {
                        'key':'nuevo_juego',
                        'desc':'Nuevo juego a reservar: '
                    },
                ]
            },
            {
                'id':'serv8',
                'desc': 'Cancelar Reserva',
                'function': lambda res: g_print('Reserva fue cancelada exitosamente') if eval(res[12:]) else f_print('No se pudo cancelar la reserva'),
                'inputs':[                    
                    {
                        'key':'titulo',
                        'desc':'Nombre del juego que reservo: '
                    },
                ]
            },
            {
                'id':'ser10',
                'desc': 'Consultar Horario',
                'user_types': [0, 1, 2],
                'function': display_horario,
                'inputs':[
                    {
                        'key':'dia_semana',
                        'desc':'Dia de la semana o vacio para consultar por todo el horario: '
                    }
                ]
            },
            {
                'id':'ser11',
                'desc': 'Editar nombre de la Reserva',
                'function': lambda res: g_print('Nombre de la reserva editada exitosamente') if eval(res[12:]) else f_print('No se pudo editar el nombre de la reserva'),
                'inputs':[
                    {
                        'key':'id',
                        'desc':'Nombre del juego que reservo: '
                    },
                    {
                        'key':'nombre_usuario',
                        'desc':'Nuevo usuario a reservar: '
                    },
                ]
            },
        ],
        admin_services=[
            {
                'id':'serv2',
                'desc': 'Agregar nuevo juego',
                'function': lambda res: g_print('Juego agregado exitosamente') if eval(res[12:]) else f_print('No se pudo agregar el juego'),
                'inputs':[
                    {
                        'key': 'titulo',
                        'desc': 'Nombre del juego: '
                    },
                    {
                        'key': 'descripcion',
                        'desc': 'Descripcion: '
                    },
                    {
                        'key':'disponibilidad',
                        'desc':'Disponibilidad [si] [no]: '
                    }
                ]
            },
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
            {
                'id':'serv5',
                'desc': 'Eliminar juego',
                'function': lambda res: g_print('Juego eliminado exitosamente') if eval(res[12:]) else f_print('No se pudo eliminar el juego'),
                'inputs':[
                    {
                        'key':'id',
                        'desc':'Nombre del juego: '
                    }
                ]
            },
            {
                'id':'serv6',
                'desc': 'Editar juego',
                'function': lambda res: g_print('Juego editado exitosamente') if eval(res[12:]) else f_print('No se pudo editar el juego'),
                'inputs':[                    
                    {
                        'key':'id',
                        'desc':'Nombre del juego a editar: '
                    },
                    {
                        'key':'nuevo_titulo',
                        'desc':'Nuevo nombre del juego o Vacio para omitir: '
                    },
                    {
                        'key':'nueva_descripcion',
                        'desc':'Nueva descripcion o vacio para omitir: '
                    },
                    {
                        'key':'nueva_disponibilidad',
                        'desc':'Disponible [si][no] o vacio para omitir: '
                    }
                ]
            },
            {
                'id':'ser12',
                'desc': 'Editar Horario',
                'function': lambda res: g_print('Horario editado exitosamente') if eval(res[12:]) else f_print('No se pudo editar el horario'),
                'inputs':[
                    {
                        'key':'dia_semana',
                        'desc':'Dia de la semana: '
                    },
                    {
                        'key':'hora_apertura',
                        'desc':'Horario de apertura: '
                    },
                    {
                        'key':'hora_cierre',
                        'desc':'Horario de cierre: '
                    },
                    {
                        'key':'es_feriado',
                        'desc':'Es feriado [si][no]: '
                    }
                ]
            },
            {
                'id':'ser10',
                'desc': 'Consultar Horario',
                'user_types': [0, 1, 2],
                'function': display_horario,
                'inputs':[
                    {
                        'key':'dia_semana',
                        'desc':'Dia de la semana o vacio para consultar por todo el horario: '
                    }
                ]
            },
            {
                'id':'serv9',
                'desc': 'Modificar fecha de prestamo',
                'function': lambda res: g_print('Fecha actualizada correctamente') if eval(res[12:]) else f_print('No se pudo actualizar la fecha'),
                'inputs':[
                    {
                        'key':'id_prestamo',
                        'desc':'ID del préstamo: '
                    },
                    {
                        'key':'nueva_fecha',
                        'desc':'Nueva fecha del préstamo en el formato DD/MM/YYYY: '
                    }
                ]
            },
            {
                'id':'ser14',
                'desc': 'Crear Multa',
                'user_types': [0, 1, 2],
                'function': display_multas,
                'inputs': [
                    {
                        'key': 'id',
                        'desc': 'vacío para consultar por todos: '
                    }
                ]
            }
        ]
    )
    res = app.show_menu()
