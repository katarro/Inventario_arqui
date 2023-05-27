from flask import Flask
import servicios.servicio_signup as Servicio
import servicios.servicio_login as ServicioLogin
import funciones.menu as Menu
import sys

app = Flask(__name__)

# Ruta para registrar al usuario
@app.route('/signup', methods=['POST'])
def signup():
    return Servicio.signup()

@app.route('/login', methods=['GET'])
def login():
    return ServicioLogin.login()

if __name__ == '__main__':
    # Obtener los datos de usuario como argumentos al ejecutar el script
    if len(sys.argv) > 1:

        opcion = sys.argv[1]

        if opcion == "inventario":
            Menu.menu()
    else:
        app.run()