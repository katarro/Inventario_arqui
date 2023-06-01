from funciones.limpiar_pantalla import limpiar_pantalla 
import requests

def funcion_inicio_sesion():
    email = input("Email: ")
    password = input("Contrasena: ")
    data = {'email': email, 'password': password}
    response = requests.get('http://localhost:5000/login', json=data)
    if response.status_code == 200:
        return response.json().get("token")
    else:
        limpiar_pantalla()
        print("Error al iniciar sesion:", response.json().get("error"))
        return None
