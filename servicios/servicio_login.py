from funciones.hashear_pass import generar_hash_sha1
from funciones.limpiar_pantalla import limpiar_pantalla 
from flask import jsonify, request
import db.conexion as Conexion
import psycopg2

def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    pass_hasheada = generar_hash_sha1(password)


    if not (pass_hasheada and email):
        response = {'error': 'Asegurese que escribio su contraseña y mail en los campos'}
        return jsonify(response), 400

    try:
        Conexion.conexion()
        Conexion.cursor.execute("SELECT * FROM usuarios WHERE correo=%s", (email,))
        Conexion.conn.commit()
        results = Conexion.cursor.fetchall()

        if not (results):
            print("El usuario ingresado no existe.")
        else:
            if(results[0][4] == pass_hasheada):
                print("Inicio de sesion exitosa.")
                # Aquí debes generar y devolver un token o identificador de sesión.
                # En este ejemplo simplificado, asumiremos que el id del usuario sirve como token.
                return jsonify({"token": results[0][1]}), 200

            else:
                return jsonify({"error": "Mail o contraseña incorrecta"}), 400

        Conexion.cursor.close()
        Conexion.conn.close()
    
    except (Exception, psycopg2.Error):
        return jsonify({'error': 'Error al conectar a la base de datos'}), 500
