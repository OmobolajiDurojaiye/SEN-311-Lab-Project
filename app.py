"""
=============================================================================
Course: MIVA-CSC312 - Web Application Development
Tutor-Marked Assessment (TMA)
Institution: MIVA Open University

Student Details:
- Name: Omobolaji Durojaiye
- Student ID: 301786646
- Matric Number: 2024/C/SENG/0814
- Date: October 23, 2026

File: app.py
Description: Main Flask application implementing:
             1. Flask setup and initialisation
             2. Homepage (index.html) with Bootstrap 5
             3. Signup page (signup.html) with form validation via request.form
             4. MySQL database connection & tbl_user table setup (username, password)
             5. Password hashing using bcrypt before database storage
=============================================================================
"""

import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash
import bcrypt
import mysql.connector
from mysql.connector import Error

# Load environment configuration if python-dotenv is present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ---------------------------------------------------------------------------
# 1. Setup & Initialisation
# ---------------------------------------------------------------------------
app = Flask(__name__)

# Secret key for session security, flash messages, and cookies
app.secret_key = os.environ.get(
    'SECRET_KEY',
    'miva-csc312-secret-key-durojaiye-301786646-2024-C-SENG-0814'
)

# MySQL Database Configuration
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_USER = os.environ.get('DB_USER', 'root')
DB_PASSWORD = os.environ.get('DB_PASSWORD', '')
DB_NAME = os.environ.get('DB_NAME', 'miva_csc312_db')
DB_PORT = int(os.environ.get('DB_PORT', 3306))

# Student Details for Display in Templates
STUDENT_DETAILS = {
    'name': 'Omobolaji Durojaiye',
    'student_id': '301786646',
    'matric': '2024/C/SENG/0814',
    'course': 'MIVA-CSC312 - Web Application Development',
    'institution': 'MIVA Open University',
    'date': 'October 23, 2026'
}


# ---------------------------------------------------------------------------
# 4. Database Integration & Setup (MySQL & tbl_user)
# ---------------------------------------------------------------------------
def setup_mysql_database():
    """
    Sets up the MySQL database and the table named `tbl_user` to store
    user information (username and password) as required by Task 4.
    """
    try:
        # Connect to MySQL server (without specifying DB first to create it if needed)
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            port=DB_PORT
        )
        cursor = conn.cursor()
        # Create database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        cursor.execute(f"USE `{DB_NAME}`;")

        # Create tbl_user table with username and password
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tbl_user (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)
        conn.commit()
        cursor.close()
        conn.close()
        print(f"[✔] MySQL Database '{DB_NAME}' and table 'tbl_user' successfully verified/created.")
        return True
    except Error as e:
        print(f"[!] MySQL Setup Notice: {e.msg} (Host: {DB_HOST}:{DB_PORT})")
        return False


def get_mysql_connection():
    """
    Connects the Flask application to the MySQL database.
    Returns (conn, None) on success or (None, error_str) on failure.
    """
    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        return conn, None
    except Error as e:
        return None, f"MySQL Connection Error [{e.errno}]: {e.msg}"


# ---------------------------------------------------------------------------
# Fallback Database Helper (Ensures the app runs seamlessly even when MySQL daemon is off)
# ---------------------------------------------------------------------------
SQLITE_DB_PATH = os.path.join(os.path.dirname(__file__), 'app_fallback.db')

def init_sqlite_fallback():
    """Fallback local database so the web application runs without crashing if MySQL is stopped."""
    with sqlite3.connect(SQLITE_DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tbl_user (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        conn.commit()


# ---------------------------------------------------------------------------
# 2. Homepage Route (index.html with HTML and Bootstrap)
# ---------------------------------------------------------------------------
@app.route('/')
def index():
    """
    Renders the basic homepage (index.html) designed with HTML and Bootstrap.
    """
    return render_template('index.html', student=STUDENT_DETAILS)


# ---------------------------------------------------------------------------
# 3. Signup Page Route & 5. Password Security (bcrypt)
# ---------------------------------------------------------------------------
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Handles user signup:
    - GET: Displays the signup form (signup.html) with `username` and `password` inputs.
    - POST: Validates form data using `request.form`, hashes password using bcrypt,
            and stores user in MySQL `tbl_user`.
    """
    if request.method == 'POST':
        # 3. Validate the form data using request.form
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        # Server-side validation
        errors = []
        if not username:
            errors.append('Username is required.')
        elif len(username) < 3:
            errors.append('Username must be at least 3 characters long.')
        elif len(username) > 50:
            errors.append('Username cannot exceed 50 characters.')

        if not password:
            errors.append('Password is required.')
        elif len(password) < 6:
            errors.append('Password must be at least 6 characters long.')

        # If validation fails, return errors to user
        if errors:
            for error in errors:
                flash(error, 'danger')
            return render_template('signup.html', username=username), 400

        # 5. Password Security: Implement password hashing with bcrypt
        # bcrypt.gensalt() generates cryptographic salt; hashpw returns hashed bytes
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        # 4. Database Integration: Store user information in MySQL tbl_user
        mysql_conn, db_err = get_mysql_connection()

        if mysql_conn:
            try:
                cursor = mysql_conn.cursor(dictionary=True)
                # Check for existing username
                cursor.execute("SELECT id FROM tbl_user WHERE username = %s", (username,))
                if cursor.fetchone():
                    flash(f"Username '{username}' is already taken. Please choose another.", 'warning')
                    cursor.close()
                    mysql_conn.close()
                    return render_template('signup.html', username=username), 409

                # Insert into MySQL tbl_user
                insert_sql = "INSERT INTO tbl_user (username, password) VALUES (%s, %s)"
                cursor.execute(insert_sql, (username, hashed_password))
                mysql_conn.commit()
                cursor.close()
                mysql_conn.close()

                flash(f"Registration successful for '{username}'! Password securely hashed with bcrypt and stored in MySQL tbl_user.", 'success')
                return redirect(url_for('view_users'))

            except Error as e:
                flash(f"MySQL Error: {e.msg}", 'danger')
                if mysql_conn.is_connected():
                    mysql_conn.close()
                return render_template('signup.html', username=username), 500
        else:
            # If MySQL is not running locally, notify user and use fallback table so app remains interactive
            try:
                init_sqlite_fallback()
                with sqlite3.connect(SQLITE_DB_PATH) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id FROM tbl_user WHERE username = ?", (username,))
                    if cursor.fetchone():
                        flash(f"Username '{username}' is already taken.", 'warning')
                        return render_template('signup.html', username=username), 409

                    cursor.execute("INSERT INTO tbl_user (username, password) VALUES (?, ?)", (username, hashed_password))
                    conn.commit()

                flash(f"User '{username}' registered with bcrypt password hashing! (Note: Saved to local mirror because MySQL at {DB_HOST}:{DB_PORT} is currently offline. Start MySQL and run setup_database.py to connect to MySQL).", 'info')
                return redirect(url_for('view_users'))
            except Exception as e:
                flash(f"Database error: {str(e)}", 'danger')
                return render_template('signup.html', username=username), 500

    # GET request: render the signup form
    return render_template('signup.html')


# ---------------------------------------------------------------------------
# Registered Users View (tbl_user verification)
# ---------------------------------------------------------------------------
@app.route('/users')
def view_users():
    """
    Displays the records from `tbl_user` to verify database integration
    and confirm that passwords are encrypted with bcrypt hashes.
    """
    mysql_conn, _ = get_mysql_connection()
    if mysql_conn:
        try:
            cursor = mysql_conn.cursor(dictionary=True)
            cursor.execute("SELECT id, username, password, created_at FROM tbl_user ORDER BY id DESC")
            records = cursor.fetchall()
            cursor.close()
            mysql_conn.close()
            return render_template('users.html', users=records, db_type='MySQL (tbl_user)', db_error=None)
        except Error as e:
            return render_template('users.html', users=[], db_type='MySQL', db_error=e.msg)
    else:
        # Fallback view if MySQL server is offline
        try:
            init_sqlite_fallback()
            with sqlite3.connect(SQLITE_DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT id, username, password, created_at FROM tbl_user ORDER BY id DESC")
                records = [dict(row) for row in cursor.fetchall()]
            return render_template('users.html', users=records, db_type='Fallback Local DB (MySQL service is offline at localhost:3306)', db_error=None)
        except Exception as e:
            return render_template('users.html', users=[], db_type='None', db_error=str(e))


# ---------------------------------------------------------------------------
# CLI Command to Run MySQL Database Setup
# ---------------------------------------------------------------------------
@app.cli.command('init-db')
def init_db_cli():
    """Run `flask init-db` to set up MySQL database and tbl_user table."""
    setup_mysql_database()


# ---------------------------------------------------------------------------
# Application Entry Point
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    # Attempt MySQL database and table setup on startup
    setup_mysql_database()
    init_sqlite_fallback()

    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true', '1')

    print("\n" + "=" * 60)
    print(" MIVA-CSC312: Web Application Development")
    print(f" Student: {STUDENT_DETAILS['name']} | ID: {STUDENT_DETAILS['student_id']}")
    print(f" Web Server Address: http://127.0.0.1:{port}/")
    print("=" * 60 + "\n")

    app.run(host='127.0.0.1', port=port, debug=debug_mode)
