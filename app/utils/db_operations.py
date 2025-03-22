import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()  # Carrega as variáveis do .env

database = os.getenv("DB_NAME", "rag_db")
user = os.getenv("DB_USER", "postgres")
host = os.getenv("DB_HOST", "db")
password = os.getenv("DB_PASSWORD", "123456")
port = os.getenv("DB_PORT", "5432")

def connect_db():
    conn = psycopg2.connect(database = database, 
                        user = user, 
                        host= host,
                        password = password,
                        port = port)

    return conn

def create_users_table(conn):
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # create table
    cur.execute("""CREATE TABLE IF NOT EXISTS users(
                user_id SERIAL PRIMARY KEY,
                user_name VARCHAR (50) UNIQUE NOT NULL,
                user_password VARCHAR (50) NOT NULL) :
                """)
    # Make the changes to the database persistent
    conn.commit()
    # Close cursor and communication with the database
    cur.close()
    conn.close()

def create_documents_table(conn):
    # Open a cursor to perform database operations
    cur = conn.cursor()
    # create table
    cur.execute("""CREATE TABLE IF NOT EXISTS documents (
                    text_id SERIAL PRIMARY KEY,  
                    text TEXT NOT NULL,
                    embedded_text VECTOR(1024) );
                """)
    # Make the changes to the database persistent
    conn.commit()
    cur.close()
    conn.close()


