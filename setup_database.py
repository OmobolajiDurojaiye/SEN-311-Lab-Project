"""
=============================================================================
Course: MIVA-CSC312 - Web Application Development
Tutor-Marked Assessment (TMA)
Student: Omobolaji Durojaiye | ID: 301786646 | Matric: 2024/C/SENG/0814

Script: setup_database.py
Task 4: Set up a MySQL database with a table named tbl_user to store
        user information (username and password).
=============================================================================
"""

import os
import mysql.connector
from mysql.connector import Error

# Load environment configuration
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', 'miva_csc312_db')
DB_PORT = int(os.environ.get('DB_PORT', 3306))


def setup_mysql_database():
    """
    Connects to MySQL server, creates the database `miva_csc312_db`,
    and creates the table `tbl_user` to store user information (username and password).
    """
    print("=" * 65)
    print("MIVA-CSC312: MySQL Database & Table Setup Script")
    print(f"Connecting to MySQL server at {DB_HOST}:{DB_PORT} as user '{DB_USER}'...")
    print("=" * 65)

    try:
        # Step 1: Connect to MySQL server (without specifying database yet)
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )

        if connection.is_connected():
            cursor = connection.cursor()
            print("[+] Successfully connected to MySQL Server.")

            # Step 2: Create the database
            print(f"[*] Creating database '{DB_NAME}' if it does not exist...")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            print(f"[+] Database '{DB_NAME}' created / verified.")

            # Step 3: Switch to the database
            cursor.execute(f"USE `{DB_NAME}`;")
            print(f"[+] Switched to database '{DB_NAME}'.")

            # Step 4: Create tbl_user table with username and password
            print("[*] Creating table 'tbl_user' (username, password)...")
            create_table_query = """
            CREATE TABLE IF NOT EXISTS tbl_user (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            cursor.execute(create_table_query)
            connection.commit()
            print("[+] Table 'tbl_user' successfully created with columns: (id, username, password, created_at)!")

            # Step 5: Describe table
            cursor.execute("DESCRIBE tbl_user;")
            columns = cursor.fetchall()
            print("\nTable Structure for tbl_user:")
            print("-" * 55)
            for col in columns:
                print(f"  Field: {col[0]:<15} Type: {col[1]:<20} Null: {col[2]}")
            print("-" * 55)

            cursor.close()
            connection.close()
            print("\n[✔] Task 4 Complete: MySQL database and 'tbl_user' table are fully set up!")
            return True

    except Error as e:
        print(f"\n[!] MySQL Connection / Setup Error [{e.errno}]: {e.msg}")
        print("[i] Hint: Please ensure your MySQL server (e.g. XAMPP, WAMP, or MySQL Service) is running on localhost:3306.")
        return False


if __name__ == '__main__':
    setup_mysql_database()
