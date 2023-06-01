from funciones.hashear_pass import generar_hash_sha1
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
    password_hasheado = generar_hash_sha1(password)

    # Verificar si se pasaron los datos como argumentos al ejecutar el script
    if not (nombre and password and email):
        return jsonify({'error': 'Faltan datos de usuario'}), 400

    try:
        Conexion.conexion()

        # Insertar el usuario en la tabla de usuarios
        Conexion.cursor.execute("INSERT INTO usuarios (nombre, apellido, correo, contrasena, tipousuario) VALUES (%s, %s, %s,%s, %s)",
        (nombre, apellido, email, password_hasheado, tipoUsuario))
        Conexion.conn.commit()

        # Cerrar la conexión
        Conexion.cursor.close()
        Conexion.conn.close()

        return jsonify({'message': 'Haz  sido  registrado'}),200
    
    except (Exception, psycopg2.Error) as error:
        # Manejo de errores
        print("Error al conectar a la base de datos:", error)
        return jsonify({'error': 'Error al conectar a la base de datos'}), 500
