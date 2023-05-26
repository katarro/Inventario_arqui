import funciones.funcion_registrar_usuario as Funciones
import funciones.funcion_inicio_sesion as InicioSesion

def menu():
    opcion = -1
    while(opcion != 3):
        print("Bienvenido al sistema de inventario")
        print("Elige una opcion: ")
        print("\t1 - Registrar usuario")
        print("\t2 - Iniciar sesion")
        print("\t3 - Crear catalogo")
        print("\t4 - Salir")
        opcion = int(input("Opcion: "))
        if opcion == 1:
            Funciones.funcion_registrar_usuario()
        elif opcion == 2:
            InicioSesion.funcion_inicio_sesion()