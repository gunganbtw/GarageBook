import pytest
from unittest.mock import patch, MagicMock
from hashlib import sha256
import psycopg2
from psycopg2 import sql
from database.GarageBase import verify_user, add_user, get_user_by_id


class TestAuthentication:
    """Tests for authentication functionality"""

    @patch('database.GarageBase.get_connection')
    def test_verify_user_success(self, mock_conn):
        """Test successful user verification"""
        # Setup mock
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1, 'testuser', 'Test User', 'test@example.com')

        # Test
        result = verify_user('testuser', 'password123')
        assert result == (1, 'testuser', 'Test User', 'test@example.com')

        # Verify SQL was called with correct parameters
        expected_hash = sha256('password123'.encode()).hexdigest()
        mock_cursor.execute.assert_called_once()

        # Get the actual SQL call
        call_args = mock_cursor.execute.call_args[0]
        assert isinstance(call_args[0], sql.SQL)
        assert call_args[1] == ('testuser', expected_hash)

    @patch('database.GarageBase.get_connection')
    def test_verify_user_failure(self, mock_conn):
        """Test failed user verification"""
        # Setup mock
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        # Test
        result = verify_user('wronguser', 'wrongpass')
        assert result is None

    @patch('database.GarageBase.get_connection')
    def test_verify_user_database_error(self, mock_conn):
        """Test database error during verification"""
        # Setup mock to raise error
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.side_effect = psycopg2.Error("Database error")

        # Test
        result = verify_user('testuser', 'password123')
        assert result is None

    @patch('database.GarageBase.get_connection')
    def test_password_hashing(self, mock_conn):
        """Test password is properly hashed"""
        # Setup mock
        test_password = "testpass123"
        expected_hash = sha256(test_password.encode()).hexdigest()

        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1, 'testuser', 'Test User', 'test@example.com')

        # Test
        verify_user('testuser', test_password)

        # Verify hash was used in query
        call_args = mock_cursor.execute.call_args[0]
        assert call_args[1][1] == expected_hash  # password_hash is second parameter

    @patch('database.GarageBase.get_connection')
    def test_add_user_success(self, mock_conn):
        """Test successful user registration"""
        # Setup mock
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        # Test
        result = add_user('newuser', 'password123', 'New User', 'new@example.com')
        assert result is True

        # Verify SQL was called with correct parameters
        expected_hash = sha256('password123'.encode()).hexdigest()
        mock_cursor.execute.assert_called_once()

        # Get the actual SQL call
        call_args = mock_cursor.execute.call_args[0]
        assert isinstance(call_args[0], sql.SQL)
        assert call_args[1] == ('newuser', expected_hash, 'New User', 'new@example.com')

    @patch('database.GarageBase.get_connection')
    def test_add_user_duplicate(self, mock_conn):
        """Test duplicate user registration"""
        # Setup mock to raise UniqueViolation
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.side_effect = psycopg2.errors.UniqueViolation("Duplicate user")

        # Test
        result = add_user('existinguser', 'password123', 'Existing User')
        assert result is False

    @patch('database.GarageBase.get_connection')
    def test_get_user_by_id(self, mock_conn):
        """Test retrieving user by ID"""
        # Setup mock
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1, 'testuser', 'Test User', 'test@example.com')

        # Test
        result = get_user_by_id(1)
        assert result == (1, 'testuser', 'Test User', 'test@example.com')