import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def obtener_conexion():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        dbname=os.getenv("DB_NAME", "ProyectoFinal")
    )

def close_connection(conn):
    if conn:
        conn.close()

