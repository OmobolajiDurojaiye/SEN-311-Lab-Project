# SEN-311-Lab-Project

# MIVA-CSC312: Web Application Development
## Tutor-Marked Assessment (TMA) - Flask Web Application

**Institution:** MIVA Open University  
**Student Name:** Omobolaji Durojaiye  
**Student ID:** 301786646  
**Matric Number:** 2024/C/SENG/0814  
**Date:** October 23, 2026  

---

## 📋 Project Overview

This project is a traditional Flask web application developed in accordance with the requirements of **MIVA-CSC312 (Web Application Development)** Tutor-Marked Assessment.

The application demonstrates core full-stack web engineering principles:
1. **Model-View-Template (MVT/MVC)** application architecture using Python Flask.
2. **Responsive Front-end Interface** built with HTML5, Jinja2 template inheritance, and Bootstrap 5.
3. **Robust Form Handling & Validation** using Flask's `request.form`.
4. **Relational Database Persistence** with MySQL connector and raw parameterized SQL queries (protecting against SQL Injection attacks).
5. **Industry-Standard Password Security** using Werkzeug's cryptographic hashing (`generate_password_hash`) before database storage.

---

## 📁 Project Directory Structure

```text
SEN 311 lab/
│
├── app.py                                   # 1. Main Flask application entry point & routes
├── setup_database.py                        # 4. Standalone Python setup script for MySQL DB & `tbl_user` table
├── schema.sql                               # 4. MySQL database & `tbl_user` table creation DDL script
├── requirements.txt                         # Project Python dependencies (Flask, bcrypt, mysql-connector-python)
├── .env.example                             # Environment variable template for DB connection
├── test_app.py                              # Automated unit & integration test suite
├── README.md                                # Comprehensive project documentation
├── miva_csc312_tutor_marked_assessment.md  # Original TMA assignment prompt
│
├── templates/                               # Jinja2 HTML templates
│   ├── base.html                            # Common base template with navbar, flash alerts & footer
│   ├── index.html                           # 2. Homepage with Bootstrap and student profile
│   ├── signup.html                          # 3. User registration form with validation
│   └── users.html                           # Verification view displaying records from `tbl_user`
│
└── static/                                  # Static assets
    └── css/
        └── style.css                        # Custom styling complementing Bootstrap 5
```

---

## 🛠️ Requirements & Implementation Details

### 1. Setup & Initialization (`app.py`)
* Initialized Flask application (`app = Flask(__name__)`).
* Configured application `secret_key` for session protection and flash alert messages.
* Integrated database credentials with fallback defaults (`localhost`, `root`, ``, `miva_csc312_db`).

### 2. Homepage (`templates/index.html`)
* Located inside the `templates/` directory.
* Designed using **Bootstrap 5.3** (via CDN), offering a modern hero banner, student information card, and navigation controls.
* Extends `templates/base.html` using Jinja2 inheritance for standard layout consistency.

### 3. Signup Page (`templates/signup.html`)
* Implemented form with input fields for `username` and `password`.
* Submits via `POST` method to the `/signup` route.
* Implements server-side validation using `request.form`:
  * Validates non-empty username and password.
  * Checks username length (minimum 3 characters, maximum 50 characters).
  * Enforces password length policy (minimum 6 characters).
  * Checks if the username already exists in `tbl_user` before insertion.
  * Displays user feedback via dismissible Bootstrap flash banners (`alert-danger`, `alert-warning`, `alert-success`).

### 4. Database Integration (`schema.sql` & `app.py`)
* Configured MySQL database named `miva_csc312_db`.
* Created table `tbl_user` defined as:
  ```sql
  CREATE TABLE IF NOT EXISTS tbl_user (
      id INT AUTO_INCREMENT PRIMARY KEY,
      username VARCHAR(100) NOT NULL UNIQUE,
      password VARCHAR(255) NOT NULL,
      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
  ```
* Connects the Flask app to MySQL using `mysql-connector-python`.
* Executes safe, parameterized SQL statements (`%s` placeholders) to prevent SQL Injection:
  ```python
  cursor.execute(
      "INSERT INTO tbl_user (username, password) VALUES (%s, %s)",
      (username, hashed_password)
  )
  ```

### 5. Password Security (`app.py` & `requirements.txt`)
* Raw user passwords are **never** stored in plain text.
* Utilizes **`bcrypt`** (`bcrypt.hashpw` with `bcrypt.gensalt()`) for salted cryptographic one-way hashing before storing credentials into `tbl_user.password`.
* Verified with `bcrypt.checkpw` in the test suite.

---

## 🚀 Getting Started & Execution Guide

### Prerequisites
* Python 3.10+ (Python 3.13 tested)
* MySQL Server (e.g. via MySQL Community Server, XAMPP, WAMP, or Docker)

### Step 1: Install Dependencies
Open your terminal inside the project directory and install the required packages:
```bash
pip install -r requirements.txt
```

### Step 2: Set Up the MySQL Database
You can create the database and table using any of the following methods:

#### Method A: Using MySQL Command Line
```bash
mysql -u root -p < schema.sql
```

#### Method B: Using phpMyAdmin or MySQL Workbench
1. Open phpMyAdmin or MySQL Workbench.
2. Open or copy the contents of `schema.sql`.
3. Execute the SQL script.

#### Method C: Using the Built-in Flask CLI
If MySQL is already running with default credentials:
```bash
flask init-db
```

### Step 3: Configure Environment Variables (Optional)
If your MySQL configuration uses a custom password or port, copy `.env.example` to `.env` and update the values:
```bash
cp .env.example .env
```
Default connection values used if `.env` is omitted:
* Host: `localhost`
* User: `root`
* Password: `""` (blank)
* Database: `miva_csc312_db`
* Port: `3306`

### Step 4: Run the Application
Start the Flask development server:
```bash
python app.py
```
Open your web browser and navigate to:
**`http://127.0.0.1:5000/`**

---

## 🧪 Running Automated Tests

A comprehensive test suite is provided in `test_app.py` covering all assessment deliverables:
```bash
python -m unittest test_app.py
```

All 6 test cases verify:
* Homepage rendering and student information display.
* Signup page form rendering.
* Server-side `request.form` validation (missing values, minimum lengths).
* Parameterized MySQL query execution and password hashing validation.
* Duplicate username handling.

---

## 📄 Submission Deliverables Checklist

| Deliverable | File Path | Status |
| :--- | :--- | :--- |
| **Main Flask Application** | `app.py` | ✅ Completed |
| **Homepage Template** | `templates/index.html` | ✅ Completed |
| **Signup Page Template** | `templates/signup.html` | ✅ Completed |
| **MySQL Table Script** | `schema.sql` | ✅ Completed |
| **Base Layout Template** | `templates/base.html` | ✅ Completed |
| **Verification / Users View** | `templates/users.html` | ✅ Completed |
| **Stylesheets** | `static/css/style.css` | ✅ Completed |
| **Automated Test Suite** | `test_app.py` | ✅ Completed |
| **Requirements Specification** | `requirements.txt` | ✅ Completed |

---
*Copyright 2024 MIVA Open University. All Rights Reserved.*
