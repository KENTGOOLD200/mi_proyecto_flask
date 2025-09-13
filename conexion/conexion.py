import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='proyecto_web',
        password='',  # sin contraseña
        database='mi_proyecto_flask'
    )
