import sqlite3
import os
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'careercast.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Resumes Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS resumes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            prediction TEXT NOT NULL,
            confidence REAL NOT NULL DEFAULT 0.0,
            accuracy REAL NOT NULL DEFAULT 92.84,
            green_flags TEXT NOT NULL,
            red_flags TEXT NOT NULL,
            parsed_entities TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
        )
    ''')

    # Check if admin user exists, if not create default admin
    cursor.execute('SELECT * FROM users WHERE email = ?', ('admin@careercast.com',))
    admin = cursor.fetchone()
    if not admin:
        hashed_pw = generate_password_hash('Admin@123456')
        cursor.execute('''
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        ''', ('System Administrator', 'admin@careercast.com', hashed_pw, 'admin'))

    # Check if demo user exists, if not create demo user
    cursor.execute('SELECT * FROM users WHERE email = ?', ('user@careercast.com',))
    demo_user = cursor.fetchone()
    if not demo_user:
        hashed_pw = generate_password_hash('User@123456')
        cursor.execute('''
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        ''', ('Demo Candidate', 'user@careercast.com', hashed_pw, 'user'))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
