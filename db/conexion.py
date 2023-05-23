import psycopg2

# Variables globales
conn = None
cursor = None

def conexion():
    global conn, cursor
    conn = psycopg2.connect(
        host='bbpzwcbmdyu2wotib6og-postgresql.services.clever-cloud.com',
        port='5432',
        database='bbpzwcbmdyu2wotib6og',
        user='uwnuqyetyjpariikmobj',
        password='Is7jUIMZs9x9QLc93kd6WuHIw85Et4'
    )
    cursor = conn.cursor()
