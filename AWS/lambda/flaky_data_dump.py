import mysql.connector
from faker import Faker
from datetime import datetime
import random

# ==============================
# CONFIGURATION
# ==============================
DB_HOST = "YOUR_EC2_PUBLIC_IP"   # e.g. 54.210.xxx.xxx
DB_NAME = "your_database"
DB_USER = "your_username"
DB_PASSWORD = "your_password"
DB_PORT = 3306
RECORD_COUNT = 1000

# ==============================
# INIT
# ==============================
fake = Faker()

def create_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )

def create_table(cursor):
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(100) UNIQUE,
            phone VARCHAR(20),
            address TEXT,
            created_at DATETIME
        )
    """)

def generate_fake_user():
    return (
        fake.first_name(),
        fake.last_name(),
        fake.unique.email(),
        fake.phone_number(),
        fake.address(),
        datetime.now()
    )

def insert_fake_data(cursor, count):
    insert_query = """
        INSERT INTO users
        (first_name, last_name, email, phone, address, created_at)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    data_batch = [generate_fake_user() for _ in range(count)]
    cursor.executemany(insert_query, data_batch)

if __name__ == "__main__":
    try:
        print("Connecting to MySQL...")
        conn = create_connection()
        cursor = conn.cursor()

        print("Creating table if not exists...")
        create_table(cursor)

        print(f"Inserting {RECORD_COUNT} fake records...")
        insert_fake_data(cursor, RECORD_COUNT)

        conn.commit()
        print("Data inserted successfully!")

    except Exception as e:
        print("Error:", e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
            print("Connection closed.")
