from flask import Flask, request, jsonify
import requests
import sys
import servicios.servicio_signup as servicio_signup

app = Flask(__name__)

# Ruta para registrar al usuario
@app.route('/signup', methods=['POST'])
def signup():
    return servicio_signup.signup()


if __name__ == '__main__':
    # Obtener los datos de usuario como argumentos al ejecutar el script
    if len(sys.argv) > 1:

        opcion = sys.argv[1]

        if opcion == 'signup':
            nombre = sys.argv[2]
            apellido = sys.argv[3]
            email = sys.argv[4]
            password = sys.argv[5]
            tipoUsuario = sys.argv[6]
            data = {'nombre': nombre, 'apellido': apellido, 'email': email, 'password': password, 'tipoUsuario': tipoUsuario}


        # Enviar una solicitud POST al endpoint de registro de usuario
        response = requests.post('http://localhost:5000/signup', json=data)

        # Mostrar la respuesta del servicio
        print(response.json())

    else:
        app.run()