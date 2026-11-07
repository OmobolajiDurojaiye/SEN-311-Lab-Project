-- ==============================================================
-- MIVA Open University
-- Course: MIVA-CSC312 - Web Application Development
-- Tutor-Marked Assessment (TMA)
-- Student Name: Omobolaji Durojaiye
-- Student ID: 301786646
-- Matric Number: 2024/C/SENG/0814
-- Date: October 23, 2026
-- ==============================================================
-- Database Schema Script: schema.sql
-- Description: Creates the database and `tbl_user` table for storing
--              user account credentials with hashed passwords.
-- ==============================================================

-- 1. Create database if it does not already exist
CREATE DATABASE IF NOT EXISTS miva_csc312_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

-- 2. Select database to use
USE miva_csc312_db;

-- 3. Create the `tbl_user` table
-- Note: password column is VARCHAR(255) to accommodate secure password hashes
-- (such as Werkzeug scrypt or pbkdf2 hashes which are typically 100-200+ characters)
CREATE TABLE IF NOT EXISTS tbl_user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 4. Verify table structure
DESCRIBE tbl_user;

-- Optional verification query:
-- SELECT * FROM tbl_user;
