import funciones.funcion_registrar_usuario as Funciones

def menu():
    opcion = -1
    while(opcion != 3):
        print("Bienvenido al sistema de inventario")
        print("Elige una opcion: ")
        print("\t1 - Registrar usuario")
        print("\t2 - Crear catalogo")
        print("\t3 - Salir")
        opcion = int(input("Opcion: "))
        if opcion == 1:
            Funciones.funcion_registrar_usuario()