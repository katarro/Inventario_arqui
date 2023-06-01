from servicios.servicio_signup import signup
from servicios.servicio_login import login
from funciones.menu import menu
from flask import Flask
import sys
app = Flask(__name__)

@app.route('/signup', methods=['POST'])
def route_signup():
    return signup()

@app.route('/login', methods=['GET'])
def route_login():
    return login()



if __name__ == '__main__':
    if len(sys.argv) > 1:
        opcion = sys.argv[1]
        if opcion == "inventario":
            menu()
    else:
        app.run()