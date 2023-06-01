from funciones.limpiar_pantalla import limpiar_pantalla 
from art import text2art
import requests


def funcion_registrar_usuario():

    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    email = input("Email: ")
    password = input("Contrasena: ")
    tipoUsuario = input("Tipo de usuario: ")
    data = {'nombre': nombre, 'apellido': apellido, 'email': email, 'password': password, 'tipoUsuario': tipoUsuario}
    response = requests.post('http://localhost:5000/signup', json=data)
    message = response.json()['message']
    limpiar_pantalla()
    print(text2art(message))