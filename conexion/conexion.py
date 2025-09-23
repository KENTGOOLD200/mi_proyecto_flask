# === Archivo: conexion/conexion.py ===
# (Se conserva tu función original y se AGREGAN helpers para usuarios)

import mysql.connector

# --- ORIGINAL TUYO (conexión a mi_proyecto_flask) ---
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='proyecto_web',
        password='',  # sin contraseña
        database='mi_proyecto_flask'
    )
