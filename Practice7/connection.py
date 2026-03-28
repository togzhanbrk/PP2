import psycopg2

def get_connection():
    conn = psycopg2.connect(
        database = "PRC7",
        user = "postgres",
        password = "postgres",
        host = "localhost",
        port = '5432'
    )
    return conn