import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='db_factura',
            user='root',
            password='',  
            port=5506      
        )
        return connection
    except Error as e:
        print(f"Error de conexión: {e}")
        return None
