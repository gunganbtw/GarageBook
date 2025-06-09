import pytest
from unittest.mock import patch, MagicMock
import psycopg2
from psycopg2 import sql
from database.GarageBase import (
    add_break_history,
    update_break_history,
    delete_break_history,
    get_break_history
)


class TestBreakHistory:
    """Тесты для работы с историей поломок"""

    @patch('database.GarageBase.get_connection')
    def test_add_break_history_success(self, mock_conn):
        """Успешное добавление записи о поломке"""
        # Настройка моков
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (1,)  # Возвращаем ID автомобиля

        # Тестовые данные
        car_id = 1
        break_desc = "Замена двигателя"
        error_code = "P0300"

        # Вызов тестируемой функции
        result = add_break_history(car_id, break_desc, error_code)

        # Проверки
        assert result == car_id
        mock_cursor.execute.assert_called_once()

        # Проверка SQL запроса
        call_args = mock_cursor.execute.call_args[0]
        assert isinstance(call_args[0], sql.SQL)
        assert call_args[1] == (car_id, break_desc, error_code)
        mock_conn.return_value.commit.assert_called_once()

    @patch('database.GarageBase.get_connection')
    def test_add_break_history_failure(self, mock_conn):
        """Ошибка при добавлении записи о поломке"""
        # Настройка моков для ошибки
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.execute.side_effect = psycopg2.Error("Database error")

        # Вызов тестируемой функции
        result = add_break_history(1, "Поломка", "P0123")

        # Проверки
        assert result is None
        mock_conn.return_value.commit.assert_not_called()

    @patch('database.GarageBase.get_connection')
    def test_update_break_history_success(self, mock_conn):
        """Успешное обновление записи о поломке"""
        # Настройка моков
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (True,)  # Успешное обновление

        # Тестовые данные
        car_id = 1
        new_desc = "Обновленное описание"
        new_code = "P0700"

        # Вызов тестируемой функции
        result = update_break_history(car_id, new_desc, new_code)

        # Проверки
        assert result is True
        mock_cursor.callproc.assert_called_once_with(
            'update_break_history',
            (car_id, new_desc, new_code)
        )
        mock_conn.return_value.commit.assert_called_once()

    @patch('database.GarageBase.get_connection')
    def test_update_break_history_partial(self, mock_conn):
        """Частичное обновление записи (только описание)"""
        # Настройка моков
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (True,)

        # Тестовые данные - обновляем только описание
        car_id = 1
        new_desc = "Новое описание"

        # Вызов тестируемой функции
        result = update_break_history(car_id, break_desc=new_desc)

        # Проверки
        assert result is True
        mock_cursor.callproc.assert_called_once_with(
            'update_break_history',
            (car_id, new_desc, None)
        )

    @patch('database.GarageBase.get_connection')
    def test_update_break_history_failure(self, mock_conn):
        """Ошибка при обновлении записи"""
        # Настройка моков для ошибки
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.callproc.side_effect = psycopg2.Error("Update error")

        # Вызов тестируемой функции
        result = update_break_history(1, "Новое описание", "P0123")

        # Проверки
        assert result is None

    @patch('database.GarageBase.get_connection')
    def test_delete_break_history_success(self, mock_conn):
        """Успешное удаление записи о поломке"""
        # Настройка моков
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchone.return_value = (True,)  # Успешное удаление

        # Тестовые данные
        car_id = 1

        # Вызов тестируемой функции
        result = delete_break_history(car_id)

        # Проверки
        assert result is True
        mock_cursor.callproc.assert_called_once_with(
            'delete_break_history',
            (car_id,)
        )
        mock_conn.return_value.commit.assert_called_once()

    @patch('database.GarageBase.get_connection')
    def test_delete_break_history_failure(self, mock_conn):
        """Ошибка при удалении записи"""
        # Настройка моков для ошибки
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.callproc.side_effect = psycopg2.Error("Delete error")

        # Вызов тестируемой функции
        result = delete_break_history(1)

        # Проверки
        assert result is None

    @patch('database.GarageBase.get_connection')
    def test_get_break_history_all(self, mock_conn):
        """Получение всей истории поломок"""
        # Настройка моков
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        # Моковые данные
        mock_data = [
            (1, "Поломка двигателя", "P0300"),
            (1, "Проблемы с трансмиссией", "P0700")
        ]
        mock_cursor.fetchall.return_value = mock_data

        # Вызов тестируемой функции
        result = get_break_history()

        # Проверки
        assert len(result) == 2
        assert result == mock_data
        mock_cursor.execute.assert_called_once()

        # Проверка SQL запроса
        call_args = mock_cursor.execute.call_args[0]
        assert isinstance(call_args[0], sql.SQL)
        assert "WHERE" not in str(call_args[0])  # Без условия WHERE

    @patch('database.GarageBase.get_connection')
    def test_get_break_history_by_car(self, mock_conn):
        """Получение истории поломок для конкретного автомобиля"""
        # Настройка моков
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor

        # Моковые данные
        mock_data = [
            (1, "Поломка двигателя", "P0300")
        ]
        mock_cursor.fetchall.return_value = mock_data

        # Тестовые данные
        car_id = 1

        # Вызов тестируемой функции
        result = get_break_history(car_id)

        # Проверки
        assert len(result) == 1
        assert result == mock_data
        mock_cursor.execute.assert_called_once()

        # Проверка SQL запроса
        call_args = mock_cursor.execute.call_args[0]
        assert isinstance(call_args[0], sql.SQL)
        assert "WHERE" in str(call_args[0])  # Должно быть условие WHERE
        assert call_args[1] == (car_id,)

    @patch('database.GarageBase.get_connection')
    def test_get_break_history_empty(self, mock_conn):
        """Получение пустой истории поломок"""
        # Настройка моков
        mock_cursor = MagicMock()
        mock_conn.return_value = MagicMock()
        mock_conn.return_value.cursor.return_value.__enter__.return_value = mock_cursor
        mock_cursor.fetchall.return_value = []

        # Вызов тестируемой функции
        result = get_break_history()

        # Проверки
        assert result == []