import psycopg2

from src.config import dbname, port, host, password, user


def get_database_connection():
    try:
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port,
        )
        print("Connected to the database successfully.")
        return connection
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

connection = get_database_connection()
