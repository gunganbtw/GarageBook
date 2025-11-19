import pytest
from unittest.mock import patch, MagicMock
import psycopg2
from psycopg2 import sql
from database.GarageBase import add_car, update_car, delete_car, get_cars, get_car_by_id


class TestCarManagement:
    """Tests for car management functionality"""

    @patch('database.GarageBase.get_connection')
    def test_add_car_success(self, mock_conn):
        """Test successful car addition"""
        # Setup mock
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        # Test data
        test_data = ("Toyota", "ABC123456", "Red", "Camry")

        # Test
        result = add_car(*test_data)
        assert result is True

        # Verify the stored procedure was called
        mock_cursor.callproc.assert_called_once_with('add_car', test_data)
        mock_conn.return_value.commit.assert_called_once()

    @patch('database.GarageBase.get_connection')
    def test_add_car_failure(self, mock_conn):
        """Test car addition failure"""
        # Setup mock to raise error
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.callproc.side_effect = psycopg2.Error("Database error")

        # Test
        result = add_car("Toyota", "ABC123456", "Red", "Camry")
        assert result is False

    @patch('database.GarageBase.get_connection')
    def test_update_car_success(self, mock_conn):
        """Test successful car update"""
        # Setup mock
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (True,)

        # Test data
        car_id = 1
        update_data = ("Toyota", "NEWVIN123", "Blue", None)

        # Test
        result = update_car(car_id, *update_data)
        assert result is True

        # Verify the stored procedure was called
        expected_args = (car_id,) + update_data
        mock_cursor.callproc.assert_called_once_with('update_car', expected_args)
        mock_conn.return_value.commit.assert_called_once()

    @patch('database.GarageBase.get_connection')
    def test_update_car_partial(self, mock_conn):
        """Test partial car update (only some fields)"""
        # Setup mock
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (True,)

        # Test data - only updating color
        car_id = 1
        update_data = (None, None, "Black", None)

        # Test
        result = update_car(car_id, *update_data)
        assert result is True

        # Verify the stored procedure was called
        expected_args = (car_id,) + update_data
        mock_cursor.callproc.assert_called_once_with('update_car', expected_args)

    @patch('database.GarageBase.get_connection')
    def test_update_car_failure(self, mock_conn):
        """Test car update failure"""
        # Setup mock to raise error
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.callproc.side_effect = psycopg2.Error("Database error")

        # Test
        result = update_car(1, "Toyota", "NEWVIN123", "Blue", "Camry")
        assert "Ошибка при обновлении автомобиля" in result

    @patch('database.GarageBase.get_connection')
    def test_delete_car_success(self, mock_conn):
        """Test successful car deletion"""
        # Setup mock
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (True,)

        # Test
        car_id = 1
        result = delete_car(car_id)
        assert result is True

        # Verify the stored procedure was called
        mock_cursor.callproc.assert_called_once_with('delete_car', (car_id,))
        mock_conn.return_value.commit.assert_called_once()

    @patch('database.GarageBase.get_connection')
    def test_delete_car_failure(self, mock_conn):
        """Test car deletion failure"""
        # Setup mock to raise error
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.callproc.side_effect = psycopg2.Error("Database error")

        # Test
        result = delete_car(1)
        assert "Ошибка при удалении автомобиля" in result

    @patch('database.GarageBase.get_connection')
    def test_get_cars(self, mock_conn):
        """Test retrieving all cars"""
        # Setup mock
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        # Mock return data
        mock_data = [
            (1, 'Toyota', 'Camry', 'ABC123', 'Red', 1),
            (2, 'Honda', 'Accord', 'DEF456', 'Blue', 1)
        ]
        mock_cursor.fetchall.return_value = mock_data

        # Test
        result = get_cars()
        assert len(result) == 2
        assert result == mock_data

        # Verify SQL was executed
        mock_cursor.execute.assert_called_once()
        assert isinstance(mock_cursor.execute.call_args[0][0], sql.SQL)

    @patch('database.GarageBase.get_connection')
    def test_get_car_by_id(self, mock_conn):
        """Test retrieving specific car by ID"""
        # Setup mock
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        # Mock return data
        mock_data = (1, 'Toyota', 'Camry', 'ABC123', 'Red')
        mock_cursor.fetchone.return_value = mock_data

        # Test
        car_id = 1
        result = get_car_by_id(car_id)
        assert result == mock_data

        # Verify SQL was executed with correct parameter
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert isinstance(call_args[0], sql.SQL)
        assert call_args[1] == (car_id,)

    @patch('database.GarageBase.get_connection')
    def test_get_car_by_id_not_found(self, mock_conn):
        """Test retrieving non-existent car"""
        # Setup mock
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = None

        # Test
        result = get_car_by_id(999)
        assert result is None