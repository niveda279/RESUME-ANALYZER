from flask import Blueprint, jsonify
from routes.auth import admin_required
from models.user import UserModel
from models.resume import ResumeModel
from utils.ml_model import get_model_metrics

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_stats(current_user):
    users = UserModel.get_all_users()
    total_users = len(users)
    total_resumes = ResumeModel.count_total()
    metrics = get_model_metrics()

    return jsonify({
        "total_users": total_users,
        "total_resumes": total_resumes,
        "accuracy": metrics.get("accuracy", 92.84),
        "metrics": metrics
    }), 200

@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users(current_user):
    users = UserModel.get_all_users()
    return jsonify({"users": users}), 200

@admin_bp.route('/user/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(current_user, user_id):
    if user_id == current_user['id']:
        return jsonify({'message': 'Cannot delete your own admin account'}), 400

    UserModel.delete_user(user_id)
    return jsonify({'message': 'User deleted successfully'}), 200

@admin_bp.route('/resumes', methods=['GET'])
@admin_required
def get_resumes(current_user):
    resumes = ResumeModel.get_all()
    return jsonify({"resumes": resumes}), 200

@admin_bp.route('/resume/<int:resume_id>', methods=['DELETE'])
@admin_required
def delete_resume(current_user, resume_id):
    ResumeModel.delete_resume(resume_id)
    return jsonify({'message': 'Resume deleted successfully'}), 200
