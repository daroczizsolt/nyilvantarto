import mysql.connector
from mysql.connector import Error

def db_connect():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="nyilvantartas"
        )
        return conn if conn.is_connected() else None
    except Error as e:
        print(f"Hiba a kapcsolódáskor: {e}")
        return None