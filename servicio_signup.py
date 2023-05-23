from flask import Flask, request, jsonify
import requests
import sys

def signup():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    print(f"Usuario: {username}")
    print(f"Contraseña: {password}")
    print(f"Email: {email}")

    # Verificar si se pasaron los datos como argumentos al ejecutar el script
    if not (username and password and email):
        response = {'error': 'Faltan datos de usuario'}
        return jsonify(response), 400

    # Lógica para registrar al usuario
    # ...

    # Respuesta de éxito
    response = {'message': 'Usuario registrado exitosamente'}
    return jsonify(response)