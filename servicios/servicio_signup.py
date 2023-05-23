from flask import request, jsonify
import db.conexion as Conexion
import psycopg2

def signup():
    data = request.json

    nombre = data.get('nombre')
    apellido = data.get('apellido')
    email = data.get('email')
    password = data.get('password')
    tipoUsuario = data.get('tipoUsuario')
    

    print(nombre, apellido, email, password, tipoUsuario)

    # Verificar si se pasaron los datos como argumentos al ejecutar el script
    if not (nombre and password and email):
        response = {'error': 'Faltan datos de usuario'}
        return jsonify(response), 400

    # Conectarse a la base de datos PostgreSQL
    try:
        # Obtener la conexión
        Conexion.conexion()

        # Insertar el usuario en la tabla de usuarios
        Conexion.cursor.execute("INSERT INTO usuarios (nombre, apellido, correo, contrasena, tipousuario) VALUES (%s, %s, %s,%s, %s)",
        (nombre, apellido, email, password, tipoUsuario))
        Conexion.conn.commit()

        # Cerrar la conexión
        Conexion.cursor.close()
        Conexion.conn.close()

        # Respuesta de éxito
        response = {'message': 'Usuario registrado exitosamente'}
        return jsonify(response)
    
    except (Exception, psycopg2.Error) as error:
        # Manejo de errores
        print("Error al conectar a la base de datos:", error)
        response = {'error': 'Error al conectar a la base de datos'}
        return jsonify(response), 500
