# === Archivo: conexion/conexion.py ===

import mysql.connector

# --- (conexión a mi_proyecto_flask) ---
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # sin contraseña
        database='mi_proyecto_flask'
    )
