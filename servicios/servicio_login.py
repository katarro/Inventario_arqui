import json
from flask import request, jsonify, session
import db.conexion as Conexion
import psycopg2

def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    print(email, password)

    # Verificar si se pasaron los datos como argumentos al ejecutar el script
    if not (password and email):
        response = {'error': 'Asegurese que escribio su contraseña y mail en los campos'}
        return jsonify(response), 400

    # Conectarse a la base de datos PostgreSQL
    try:
        # Obtener la conexión
        Conexion.conexion()

        # Seleccionar al usuario en la tabla de usuarios
        Conexion.cursor.execute("SELECT * FROM usuarios WHERE CorreoElectronico=%s",
        (email))
        Conexion.conn.commit()

        results = Conexion.cursor.fetchall()
        print(results)
        # Comprobar si el usuario existe
        if not (results):
            print("El usuario ingresado no existe.")
        else:
            # Autenticacion del usuario
            if(results[0][4] == password):
                print("Inicio de sesion exitosa.")
                session["usuario"] = results[0]
                #return redirect("/UserMenu")
            else:
                print("Mail o contraseña incorrecta. Intente nuevamente.")
                #redirect("/Menu")

        # Cerrar la conexión
        Conexion.cursor.close()
        Conexion.conn.close()
    
    except (Exception, psycopg2.Error) as error:
        # Manejo de errores
        print("Error al conectar a la base de datos:", error)
        response = {'error': 'Error al conectar a la base de datos'}
        return jsonify(response), 500
