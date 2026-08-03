import jwt
import datetime
from functools import wraps
from flask import Blueprint, request, jsonify, current_app
from models.user import UserModel

auth_bp = Blueprint('auth', __name__)
SECRET_KEY = 'careercast_jwt_secret_key_change_in_production'

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        if not token:
            return jsonify({'message': 'Authentication token is missing'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = UserModel.find_by_id(data['user_id'])
            if not current_user:
                return jsonify({'message': 'User not found'}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid authentication token'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        if not token:
            return jsonify({'message': 'Authentication token is missing'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = UserModel.find_by_id(data['user_id'])
            if not current_user or current_user['role'] != 'admin':
                return jsonify({'message': 'Admin privileges required'}), 403
        except Exception:
            return jsonify({'message': 'Invalid authentication token'}), 401

        return f(current_user, *args, **kwargs)
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    name = data.get('name', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not name or not email or not password:
        return jsonify({'message': 'Name, email, and password are required'}), 400

    if UserModel.find_by_email(email):
        return jsonify({'message': 'Email address already registered'}), 409

    user = UserModel.create_user(name, email, password, role='user')
    token = jwt.encode({
        'user_id': user['id'],
        'role': user['role'],
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
    }, SECRET_KEY, algorithm='HS256')

    return jsonify({
        'message': 'Registration successful',
        'token': token,
        'user': user
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')

    if not email or not password:
        return jsonify({'message': 'Email and password are required'}), 400

    user = UserModel.find_by_email(email)
    if not user or not UserModel.verify_password(user['password'], password):
        return jsonify({'message': 'Invalid email or password'}), 401

    token = jwt.encode({
        'user_id': user['id'],
        'role': user['role'],
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7)
    }, SECRET_KEY, algorithm='HS256')

    user_info = {
        'id': user['id'],
        'name': user['name'],
        'email': user['email'],
        'role': user['role']
    }

    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': user_info
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@token_required
def profile(current_user):
    return jsonify({'user': current_user}), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    return jsonify({'message': 'Logout successful'}), 200
