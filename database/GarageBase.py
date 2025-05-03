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
                SELECT user_id, full_name FROM users 
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



init_db()