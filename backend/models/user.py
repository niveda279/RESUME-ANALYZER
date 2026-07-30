from utils.database import get_db_connection
from werkzeug.security import generate_password_hash, check_password_hash

class UserModel:
    @staticmethod
    def create_user(name, email, password, role='user'):
        conn = get_db_connection()
        cursor = conn.cursor()
        hashed = generate_password_hash(password)
        try:
            cursor.execute('''
                INSERT INTO users (name, email, password, role)
                VALUES (?, ?, ?, ?)
            ''', (name, email, hashed, role))
            conn.commit()
            user_id = cursor.lastrowid
            conn.close()
            return {"id": user_id, "name": name, "email": email, "role": role}
        except Exception as e:
            conn.close()
            raise e

    @staticmethod
    def find_by_email(email):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def find_by_id(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email, role, created_at FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_all_users():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT id, name, email, role, created_at FROM users ORDER BY id DESC')
        users = cursor.fetchall()
        conn.close()
        return [dict(u) for u in users]

    @staticmethod
    def delete_user(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def verify_password(stored_password, provided_password):
        return check_password_hash(stored_password, provided_password)
