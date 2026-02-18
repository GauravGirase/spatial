import mysql.connector
from mysql.connector import Error

# ==============================
# CONFIGURATION
# ==============================
RDS_HOST = "database-1.cbys0gc46lj8.ap-south-1.rds.amazonaws.com"
RDS_PORT = 3306
RDS_USER = "admin"          # user created for DMS
RDS_PASSWORD = "*****"
RDS_DB = "testdb"

QUERY = "SELECT * FROM users LIMIT 10;"  # change table as needed

# ==============================
# FUNCTION TO CONNECT AND QUERY
# ==============================
def verify_migration():
    try:
        print(f"Connecting to RDS instance {RDS_HOST} ...")
        conn = mysql.connector.connect(
            host=RDS_HOST,
            port=RDS_PORT,
            user=RDS_USER,
            password=RDS_PASSWORD,
            database=RDS_DB
        )

        if conn.is_connected():
            print("Connection successful!")

            cursor = conn.cursor()
            cursor.execute(QUERY)

            rows = cursor.fetchall()
            print(f"Fetched {len(rows)} rows:\n")
            for row in rows:
                print(row)

    except Error as e:
        print("Error while connecting to RDS:", e)

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()
            print("Connection closed.")

# ==============================
# MAIN
# ==============================
if __name__ == "__main__":
    verify_migration()
