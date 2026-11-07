"""
=============================================================================
Course: MIVA-CSC312 - Web Application Development
Tutor-Marked Assessment (TMA) - Automated Test Suite
Student: Omobolaji Durojaiye | ID: 301786646 | Matric: 2024/C/SENG/0814
=============================================================================
"""

import unittest
from unittest.mock import MagicMock, patch
import bcrypt
from app import app


class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client and configure application for testing."""
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_homepage_renders_correctly(self):
        """Requirement 2: Verify Homepage (index.html) loads with Bootstrap & student details."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Web Application Development', response.data)
        self.assertIn(b'Omobolaji Durojaiye', response.data)
        self.assertIn(b'301786646', response.data)
        self.assertIn(b'2024/C/SENG/0814', response.data)
        self.assertIn(b'bootstrap', response.data.lower())

    def test_signup_page_renders_form(self):
        """Requirement 3: Verify Signup Page (signup.html) contains username and password inputs."""
        response = self.client.get('/signup')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'name="username"', response.data)
        self.assertIn(b'name="password"', response.data)
        self.assertIn(b'Create Account', response.data)

    def test_signup_validation_missing_fields(self):
        """Requirement 3: Validate form data using request.form (missing username & password)."""
        response = self.client.post('/signup', data={'username': '', 'password': ''})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Username is required.', response.data)
        self.assertIn(b'Password is required.', response.data)

    def test_signup_validation_short_password(self):
        """Requirement 3: Validate minimum password length rule."""
        response = self.client.post('/signup', data={'username': 'john_doe', 'password': '123'})
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'Password must be at least 6 characters long.', response.data)

    @patch('app.get_mysql_connection')
    def test_signup_bcrypt_password_hashing_and_mysql_insert(self, mock_get_conn):
        """Requirements 4 & 5: Verify bcrypt password hashing and MySQL insertion into tbl_user."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None  # Username does not exist
        mock_get_conn.return_value = (mock_conn, None)

        raw_password = 'MySecretPassword123!'
        response = self.client.post('/signup', data={
            'username': 'miva_user',
            'password': raw_password
        }, follow_redirects=False)

        # Should redirect after successful creation
        self.assertEqual(response.status_code, 302)

        # Check duplicate check query
        mock_cursor.execute.assert_any_call(
            'SELECT id FROM tbl_user WHERE username = %s',
            ('miva_user',)
        )

        # Extract and verify INSERT query
        insert_calls = [c for c in mock_cursor.execute.call_args_list if 'INSERT INTO tbl_user' in str(c[0][0])]
        self.assertTrue(len(insert_calls) > 0, "INSERT INTO tbl_user was not called.")
        sql, params = insert_calls[0][0]
        inserted_username, stored_hash = params

        self.assertEqual(inserted_username, 'miva_user')
        self.assertNotEqual(stored_hash, raw_password, "Password MUST be hashed, not stored plain text!")
        # Verify with bcrypt.checkpw
        self.assertTrue(bcrypt.checkpw(raw_password.encode('utf-8'), stored_hash.encode('utf-8')),
                        "Hash must verify with bcrypt.checkpw")
        mock_conn.commit.assert_called_once()

    @patch('app.get_mysql_connection')
    def test_signup_duplicate_username_warning(self, mock_get_conn):
        """Verify proper warning when username already exists."""
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = {'id': 1}  # Existing user found
        mock_get_conn.return_value = (mock_conn, None)

        response = self.client.post('/signup', data={
            'username': 'existing_user',
            'password': 'Password123'
        })
        self.assertEqual(response.status_code, 409)
        self.assertIn(b'already taken', response.data)


if __name__ == '__main__':
    unittest.main()
