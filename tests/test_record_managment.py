import pytest
from unittest.mock import patch, MagicMock
import psycopg2
from database.GarageBase import (
    add_service_history,
    update_service_history,
    delete_service_history
)


class TestServiceHistoryManagement:
    """Тесты для управления записями о замене расходников"""

    @patch('database.GarageBase.get_connection')
    def test_add_service_history_success(self, mock_conn):
        """Успешное добавление записи о замене расходников"""
        # Настройка моков
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        # Тестовые данные
        car_id = 1
        motor_oil = "5W-30"
        air_filter = "BOSCH F123"

        # Вызов тестируемой функции
        result = add_service_history(car_id, motor_oil, air_filter)

        # Проверки
        assert result is True
        mock_cursor.callproc.assert_called_once_with(
            'add_servis_history',
            (car_id, motor_oil, air_filter)
        )
        mock_conn.return_value.commit.assert_called_once()

    @patch('database.GarageBase.get_connection')
    def test_add_service_history_failure(self, mock_conn):
        """Ошибка при добавлении записи о замене расходников"""
        # Настройка моков для ошибки
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.callproc.side_effect = psycopg2.Error("Database error")

        # Вызов тестируемой функции
        result = add_service_history(1, "5W-30", "BOSCH F123")

        # Проверки
        assert result is False
        mock_conn.return_value.commit.assert_not_called()

    @patch('database.GarageBase.get_connection')
    def test_update_service_history_success(self, mock_conn):
        """Успешное обновление записи о замене расходников"""
        # Настройка моков
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ("Success",)

        # Тестовые данные
        old_car_id = 1
        new_data = {
            'new_car_id': 2,
            'motor_oil': "5W-40",
            'air_filter': "MANN C123",
            'transmission_oil': "75W-90",
            'cabin_filter': "FRAM CF123",
            'oil_filter': "MAHLE OX123",
            'fuel_filter': "BOSCH F456",
            'mileage': 50000
        }

        # Вызов тестируемой функции
        result = update_service_history(old_car_id, **new_data)

        # Проверки
        assert result == "Success"
        mock_cursor.callproc.assert_called_once_with(
            'update_service_history',
            (old_car_id, 2, "5W-40", "MANN C123", "75W-90",
             "FRAM CF123", "MAHLE OX123", "BOSCH F456", 50000)
        )
        mock_conn.return_value.commit.assert_called_once()

    @patch('database.GarageBase.get_connection')
    def test_update_service_history_partial(self, mock_conn):
        """Частичное обновление записи (только моторное масло)"""
        # Настройка моков
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ("Success",)

        # Тестовые данные - обновляем только моторное масло
        old_car_id = 1
        motor_oil = "5W-40"

        # Вызов тестируемой функции
        result = update_service_history(old_car_id, motor_oil=motor_oil)

        # Проверки
        assert result == "Success"
        # Проверяем что None передается для необновляемых полей
        mock_cursor.callproc.assert_called_once_with(
            'update_service_history',
            (old_car_id, None, motor_oil, None, None, None, None, None, None)
        )

    @patch('database.GarageBase.get_connection')
    def test_update_service_history_failure(self, mock_conn):
        """Ошибка при обновлении записи"""
        # Настройка моков для ошибки
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.callproc.side_effect = psycopg2.Error("Update error")

        # Вызов тестируемой функции
        result = update_service_history(1, motor_oil="5W-40")

        # Проверки
        assert "Ошибка при обновлении" in result

    @patch('database.GarageBase.get_connection')
    def test_delete_service_history_success(self, mock_conn):
        """Успешное удаление записи о замене расходников"""
        # Настройка моков
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = ("Success",)

        # Тестовые данные
        car_id = 1

        # Вызов тестируемой функции
        result = delete_service_history(car_id)

        # Проверки
        assert result == "Success"
        mock_cursor.callproc.assert_called_once_with(
            'delete_service_history',
            (car_id,)
        )
        mock_conn.return_value.commit.assert_called_once()

    @patch('database.GarageBase.get_connection')
    def test_delete_service_history_failure(self, mock_conn):
        """Ошибка при удалении записи"""
        # Настройка моков для ошибки
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.callproc.side_effect = psycopg2.Error("Delete error")

        # Вызов тестируемой функции
        result = delete_service_history(1)

        # Проверки
        assert "Ошибка при удалении" in result