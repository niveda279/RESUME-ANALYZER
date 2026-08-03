import unittest
import json
import os
import sys

# Ensure backend path is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from utils.database import init_db

class CareerCastAPITestCase(unittest.TestCase):
    def setUp(self):
        init_db()
        self.app = app.test_client()
        self.app.testing = True

    def test_health_endpoint(self):
        response = self.app.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertEqual(data['service'], 'CareerCast API')

    def test_admin_login(self):
        response = self.app.post('/api/login', data=json.dumps({
            'email': 'admin@careercast.com',
            'password': 'Admin@123456'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('token', data)
        self.assertEqual(data['user']['role'], 'admin')

    def test_user_login(self):
        response = self.app.post('/api/login', data=json.dumps({
            'email': 'user@careercast.com',
            'password': 'User@123456'
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('token', data)
        self.assertEqual(data['user']['role'], 'user')

if __name__ == '__main__':
    unittest.main()
