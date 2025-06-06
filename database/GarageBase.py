# db_postgres.py
import psycopg2
from psycopg2 import sql, errors
from hashlib import sha256
from database.dbconf import DB_CONFIG


def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except psycopg2.Error as e:
        print(f"Ошибка подключения к PostgreSQL: {e}")
        return None


def init_db():
    conn = get_connection()
    if not conn:
        return False
    conn.close()


def add_user(username, password, full_name, email=None):
    password_hash = sha256(password.encode()).hexdigest()
    conn = get_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL('''
                INSERT INTO users (username, password_hash, full_name, email)
                VALUES (%s, %s, %s, %s)
                '''),
                (username, password_hash, full_name, email)
            )
            conn.commit()
            return True
    except errors.UniqueViolation:
        return False
    except psycopg2.Error as e:
        print(f"Ошибка при добавлении пользователя: {e}")
        return False
    finally:
        conn.close()


def verify_user(username, password):
    password_hash = sha256(password.encode()).hexdigest()
    conn = get_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL('''
                SELECT user_id, username, full_name, email FROM users 
                WHERE username = %s AND password_hash = %s
                '''),
                (username, password_hash)
            )
            return cursor.fetchone()
    except psycopg2.Error as e:
        print(f"Ошибка при проверке пользователя: {e}")
        return None
    finally:
        conn.close()


def get_user_by_id(user_id):
    conn = get_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL('''
                SELECT user_id, username, full_name, email FROM users 
                WHERE user_id = %s
                '''),
                (user_id,)
            )
            return cursor.fetchone()
    except psycopg2.Error as e:
        print(f"Ошибка при получении пользователя: {e}")
        return None
    finally:
        conn.close()


def add_car(car_brand, vin, color, model):
    """Добавление нового автомобиля"""
    conn = get_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.callproc('add_car', (car_brand, vin, color, model))
            conn.commit()
            return True
    except psycopg2.Error as e:
        print(f"Ошибка при добавлении автомобиля: {e}")
        return False
    finally:
        conn.close()


def update_car(car_id, car_brand=None, vin=None, color=None, model=None):
    """Обновление данных автомобиля"""
    conn = get_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.callproc('update_car', (car_id, car_brand, vin, color, model))
            result = cursor.fetchone()[0]
            conn.commit()
            return result
    except psycopg2.Error as e:
        print(f"Ошибка при обновлении автомобиля: {e}")
        return f"Ошибка при обновлении автомобиля: {e}"
    finally:
        conn.close()


def delete_car(car_id):
    """Удаление автомобиля и всех связанных записей"""
    conn = get_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.callproc('delete_car', (car_id,))
            result = cursor.fetchone()[0]
            conn.commit()
            return result
    except psycopg2.Error as e:
        print(f"Ошибка при удалении автомобиля: {e}")
        return f"Ошибка при удалении автомобиля: {e}"
    finally:
        conn.close()


def add_break_history(car_id, break_desc, error_code):
    """Добавление записи в историю поломок"""
    conn = get_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL('''
                INSERT INTO break_history (car_id, break, error_code)
                VALUES (%s, %s, %s)
                RETURNING car_id
                '''),
                (car_id, break_desc, error_code)
            )
            conn.commit()
            return cursor.fetchone()[0]
    except psycopg2.Error as e:
        print(f"Ошибка при добавлении записи о поломке: {e}")
        return None
    finally:
        conn.close()


def update_break_history(car_id, break_desc=None, error_code=None):
    """Обновление записи в истории поломок"""
    conn = get_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.callproc('update_break_history', (car_id, break_desc, error_code))
            result = cursor.fetchone()[0]
            conn.commit()
            return result
    except psycopg2.Error as e:
        print(f"Ошибка при обновлении записи о поломке: {e}")
        return None
    finally:
        conn.close()


def delete_break_history(car_id):
    """Удаление записи из истории поломок"""
    conn = get_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.callproc('delete_break_history', (car_id,))
            result = cursor.fetchone()[0]
            conn.commit()
            return result
    except psycopg2.Error as e:
        print(f"Ошибка при удалении записи о поломке: {e}")
        return None
    finally:
        conn.close()


def get_break_history(car_id=None):
    """Получение истории поломок"""
    conn = get_connection()
    if not conn:
        return []

    try:
        with conn.cursor() as cursor:
            if car_id:
                cursor.execute(
                    sql.SQL('''
                    SELECT car_id, break, error_code FROM break_history
                    WHERE car_id = %s
                    '''),
                    (car_id,)
                )
            else:
                cursor.execute(
                    sql.SQL('''
                    SELECT car_id, break, error_code FROM break_history
                    ''')
                )
            return cursor.fetchall()
    except psycopg2.Error as e:
        print(f"Ошибка при получении истории поломок: {e}")
        return []
    finally:
        conn.close()


def get_cars():
    """Получение списка всех автомобилей"""
    conn = get_connection()
    if not conn:
        return []

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL('''
                SELECT car_id, car_brand, car_model, vin_code, car_color FROM car
                ''')
            )
            return cursor.fetchall()
    except psycopg2.Error as e:
        print(f"Ошибка при получении списка автомобилей: {e}")
        return []
    finally:
        conn.close()


def get_car_by_id(car_id):
    """Получение данных конкретного автомобиля"""
    conn = get_connection()
    if not conn:
        return None

    try:
        with conn.cursor() as cursor:
            cursor.execute(
                sql.SQL('''
                SELECT car_id, car_brand, car_model, vin_code, car_color FROM car
                WHERE car_id = %s
                '''),
                (car_id,)
            )
            return cursor.fetchone()
    except psycopg2.Error as e:
        print(f"Ошибка при получении данных автомобиля: {e}")
        return None
    finally:
        conn.close()

def add_service_history(car_id, motor_oil, air_filter):
    """Добавление записи об обслуживании"""
    conn = get_connection()
    if not conn:
        return False

    try:
        with conn.cursor() as cursor:
            cursor.callproc('add_servis_history', (car_id, motor_oil, air_filter))
            conn.commit()
            return True
    except psycopg2.Error as e:
        print(f"Ошибка при добавлении записи об обслуживании: {e}")
        return False
    finally:
        conn.close()


def delete_service_history(car_id):
    """Удаление записи об обслуживании"""
    conn = get_connection()
    if not conn:
        return "Ошибка подключения"

    try:
        with conn.cursor() as cursor:
            cursor.callproc('delete_service_history', (car_id,))
            result = cursor.fetchone()[0]
            conn.commit()
            return result
    except psycopg2.Error as e:
        print(f"Ошибка при удалении записи об обслуживании: {e}")
        return f"Ошибка при удалении: {e}"
    finally:
        conn.close()


def update_service_history(old_car_id, new_car_id=None, motor_oil=None, air_filter=None):
    """Обновление записи об обслуживании"""
    conn = get_connection()
    if not conn:
        return "Ошибка подключения"

    try:
        with conn.cursor() as cursor:
            cursor.callproc('update_service_history', (old_car_id, new_car_id, motor_oil, air_filter))
            result = cursor.fetchone()[0]
            conn.commit()
            return result
    except psycopg2.Error as e:
        print(f"Ошибка при обновлении записи об обслуживании: {e}")
        return f"Ошибка при обновлении: {e}"
    finally:
        conn.close()

init_db()