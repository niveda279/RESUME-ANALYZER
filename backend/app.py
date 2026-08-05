import os
import sys

# Ensure backend/ directory is always on Python's path,
# regardless of where gunicorn/python is invoked from.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS
from utils.database import init_db
from routes.auth import auth_bp
from routes.resume import resume_bp
from routes.admin import admin_bp

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='/')

# Config
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, '..', 'uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10 MB Max limit

# Enable CORS for frontend integration
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(resume_bp, url_prefix='/api')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "CareerCast API",
        "model": "Logistic Regression"
    }), 200

# Error Handler for Payload Too Large
@app.errorhandler(413)
def request_entity_too_large(error):
    return jsonify({'message': 'File size exceeds maximum limit of 10MB'}), 413

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return app.send_static_file(path)
    else:
        return app.send_static_file('index.html')

# Initialize SQLite Database (runs on module load — works with gunicorn too)
init_db()

if __name__ == '__main__':
    print("Starting CareerCast Flask Backend on http://127.0.0.1:5000 ...")
    app.run(host='0.0.0.0', port=5000, debug=True)
