import requests

def funcion_inicio_sesion():
    email = input("Email: ")
    password = input("Contrasena: ")
    data = {'email': email, 'password': password}
    response = requests.get('http://localhost:5000/login', json=data)
    print(response.content)