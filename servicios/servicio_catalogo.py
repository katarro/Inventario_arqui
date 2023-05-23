from flask import Flask, request, jsonify
import requests
import psycopg2
import sys

def crear_catalogo():
    data = request.json
    titulo = data.get('titulo')
    descripcion = data.get('descripcion')
    disponibilidad = data.get('disponibilidad')

    # Verificar si se pasaron los datos necesarios
    if not (titulo and descripcion and disponibilidad):
        response = {'error': 'Faltan datos para crear el catálogo'}
        return jsonify(response), 400

    # Conectar a la base de datos
    try:
        conn = psycopg2.connect(
            host='bbpzwcbmdyu2wotib6og-postgresql.services.clever-cloud.com',
            port='5432',
            database='bbpzwcbmdyu2wotib6og',
            user='uwnuqyetyjpariikmobj',
            password='Is7jUIMZs9x9QLc93kd6WuHIw85Et4'
        )
        cursor = conn.cursor()

        # Insertar el catálogo en la tabla "catalogos"
        cursor.execute("INSERT INTO catalogos (titulo, descripcion, disponibilidad) VALUES (%s, %s, %s)",
        (titulo, descripcion, disponibilidad))
        conn.commit()

        # Cerrar la conexión
        cursor.close()
        conn.close()

        # Respuesta de éxito
        response = {'message': 'Catálogo creado exitosamente'}
        return jsonify(response)
    except (Exception, psycopg2.Error) as error:
        # Manejo de errores
        print("Error al conectar a la base de datos:", error)
        response = {'error': 'Error al conectar a la base de datos'}
        return jsonify(response), 500
