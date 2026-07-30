import json
from utils.database import get_db_connection

class ResumeModel:
    @staticmethod
    def save_resume(user_id, filename, prediction, confidence, accuracy, green_flags, red_flags, parsed_entities):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO resumes (user_id, filename, prediction, confidence, accuracy, green_flags, red_flags, parsed_entities)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            user_id,
            filename,
            prediction,
            confidence,
            accuracy,
            json.dumps(green_flags),
            json.dumps(red_flags),
            json.dumps(parsed_entities)
        ))
        conn.commit()
        resume_id = cursor.lastrowid
        conn.close()
        return resume_id

    @staticmethod
    def get_by_user(user_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, user_id, filename, prediction, confidence, accuracy, green_flags, red_flags, parsed_entities, created_at
            FROM resumes
            WHERE user_id = ?
            ORDER BY id DESC
        ''', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        results = []
        for r in rows:
            d = dict(r)
            d['green_flags'] = json.loads(d['green_flags']) if d['green_flags'] else []
            d['red_flags'] = json.loads(d['red_flags']) if d['red_flags'] else []
            d['parsed_entities'] = json.loads(d['parsed_entities']) if d['parsed_entities'] else {}
            results.append(d)
        return results

    @staticmethod
    def get_by_id(resume_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM resumes WHERE id = ?', (resume_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            d = dict(row)
            d['green_flags'] = json.loads(d['green_flags']) if d['green_flags'] else []
            d['red_flags'] = json.loads(d['red_flags']) if d['red_flags'] else []
            d['parsed_entities'] = json.loads(d['parsed_entities']) if d['parsed_entities'] else {}
            return d
        return None

    @staticmethod
    def get_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT r.id, r.filename, r.prediction, r.confidence, r.accuracy, r.created_at, u.name as user_name, u.email as user_email
            FROM resumes r
            JOIN users u ON r.user_id = u.id
            ORDER BY r.id DESC
        ''')
        rows = cursor.fetchall()
        conn.close()
        return [dict(r) for r in rows]

    @staticmethod
    def delete_resume(resume_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM resumes WHERE id = ?', (resume_id,))
        conn.commit()
        conn.close()
        return True

    @staticmethod
    def count_total():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as total FROM resumes')
        res = cursor.fetchone()
        conn.close()
        return res['total'] if res else 0
