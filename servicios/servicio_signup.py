from flask import Flask, request, jsonify
import requests
import psycopg2
import sys

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
        conn = psycopg2.connect(
            host='bbpzwcbmdyu2wotib6og-postgresql.services.clever-cloud.com',
            port='5432',
            database='bbpzwcbmdyu2wotib6og',
            user='uwnuqyetyjpariikmobj',
            password='Is7jUIMZs9x9QLc93kd6WuHIw85Et4'
        )
        cursor = conn.cursor()

        # Insertar el usuario en la tabla de usuarios
        cursor.execute("INSERT INTO usuarios (nombre, apellido, correo, contrasena, tipousuario) VALUES (%s, %s, %s,%s, %s)",
        (nombre, apellido, email, password, tipoUsuario))
        conn.commit()

        # Cerrar la conexión
        cursor.close()
        conn.close()

        # Respuesta de éxito
        response = {'message': 'Usuario registrado exitosamente'}
        return jsonify(response)
    
    except (Exception, psycopg2.Error) as error:
        # Manejo de errores
        print("Error al conectar a la base de datos:", error)
        response = {'error': 'Error al conectar a la base de datos'}
        return jsonify(response), 500
