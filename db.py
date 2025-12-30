import mysql.connector
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def get_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    create table if not exists users(
                   id int auto_increment primary key,
                   name varchar(100) not null,
                   email varchar(100) unique not null,
                   age int)
""")
    conn.commit()
    cursor.close()
    conn.close()

    
