from funciones.funcion_registrar_usuario import funcion_registrar_usuario
from funciones.funcion_inicio_sesion import funcion_inicio_sesion
from funciones.limpiar_pantalla import limpiar_pantalla
from art import text2art

def menu():
    token = None
    print(text2art("Bienvenido"))
    while True:
        print("1- Registrar usuario")
        print("2- Iniciar sesion")
        print("3- Crear catalogo")
        print("4- Salir\n")
        opcion = int(input("Opcion: "))
        if opcion == 1:
            funcion_registrar_usuario()

        elif opcion == 2:
            token = funcion_inicio_sesion()
            if token is not None:
                userMenu(token)

        elif opcion == 3:
            if token is not None:
                # Aquí tendrías que implementar la lógica para crear un catálogo
                print("Crear sistema para crear catalogo")
            else:
                print("Debes iniciar sesión primero.")
                
        elif opcion == 4:
            print("Adios")
            break



def userMenu(token):
    limpiar_pantalla()
    while True:
        print(text2art(f"Hola   {token}"))
        print("Elige una opción:")
        print("1. Opción 1")
        print("2. Opción 2")
        print("3. Cerrar sesión")
        opcion = input("Opción: ")
        if opcion == '1':
            # Aquí se ejecutaría el código para la Opción 1
            print("Elegiste la Opción 1")
        elif opcion == '2':
            # Aquí se ejecutaría el código para la Opción 2
            print("Elegiste la Opción 2")
        elif opcion == '3':
            print("Has cerrado sesión.")
            break
        else:
            print("Opción inválida. Inténtalo de nuevo.")
