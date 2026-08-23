import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from routes.auth import token_required
from utils.parser import extract_text_from_file, parse_resume_text
from utils.feature_extractor import evaluate_flags
from utils.ml_model import predict_career_role, get_model_metrics, get_all_metrics
from utils.ml_service import predict_all_models
from models.resume import ResumeModel

resume_bp = Blueprint('resume', __name__)
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}
MAX_FILE_SIZE_MB = 10

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@resume_bp.route('/upload', methods=['POST'])
@token_required
def upload_resume(current_user):
    file = None
    if 'file' in request.files:
        file = request.files['file']
    elif len(request.files) > 0:
        file = list(request.files.values())[0]

    if not file or file.filename == '':
        return jsonify({'message': 'No file submitted in request'}), 400

    if not allowed_file(file.filename):
        return jsonify({'message': 'Invalid file type. Supported formats are PDF and DOCX'}), 400

    try:
        upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        filename = secure_filename(file.filename)
        if not filename:
            filename = "uploaded_resume.pdf"
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)

        # 1. Parse text from file
        raw_text = extract_text_from_file(filepath)
        if not raw_text or raw_text.startswith("Error"):
            return jsonify({'message': f'Failed to parse resume document: {raw_text}'}), 422

        # 2. Extract Entities
        parsed = parse_resume_text(raw_text)

        # 3. Dynamic Green & Red Flags
        flags = evaluate_flags(parsed)

        # 4. ML Predictions — All 3 models
        all_predictions = predict_all_models(raw_text)

        # Backward-compat: use LR result as the primary prediction
        lr_result = all_predictions.get("logistic_regression", {})
        best_result = all_predictions.get("best_prediction", lr_result)
        metrics = get_model_metrics()
        all_metrics = get_all_metrics()

        parsed_entities = {
            "name": str(parsed.get("name", "Not Provided")),
            "email": str(parsed.get("email", "Not Provided")),
            "phone": str(parsed.get("phone", "Not Provided")),
            "skills": [str(s) for s in parsed.get("skills", [])],
            "education": str(parsed.get("education", "")),
            "experience": str(parsed.get("experience", "")),
            "certifications": str(parsed.get("certifications", "")),
            "projects": str(parsed.get("projects", ""))
        }

        # 5. Save to database (use best model prediction as primary)
        resume_id = ResumeModel.save_resume(
            user_id=current_user['id'],
            filename=filename,
            prediction=str(best_result.get('predicted_role', lr_result.get('predicted_role', 'Unknown'))),
            confidence=float(best_result.get('confidence', lr_result.get('confidence', 0))),
            accuracy=float(metrics.get('accuracy', 0)),
            green_flags=[str(f) for f in flags['green_flags']],
            red_flags=[str(f) for f in flags['red_flags']],
            parsed_entities=parsed_entities
        )

        response_data = {
            "id": resume_id,
            "filename": filename,
            "parsed_entities": parsed_entities,
            "prediction": {
                "predicted_role": str(best_result.get('predicted_role', lr_result.get('predicted_role', 'Unknown'))),
                "confidence": float(best_result.get('confidence', lr_result.get('confidence', 0))),
                "breakdown": [
                    {"role": str(item['role']), "probability": float(item['probability'])}
                    for item in best_result.get('breakdown', lr_result.get('breakdown', []))
                ]
            },
            "all_predictions": {
                "logistic_regression": all_predictions.get("logistic_regression", {}),
                "random_forest": all_predictions.get("random_forest", {}),
                "xgboost": all_predictions.get("xgboost", {}),
                "best_model": all_predictions.get("best_model", "Logistic Regression"),
                "best_model_key": all_predictions.get("best_model_key", "logistic_regression"),
            },
            "model_performance": metrics,
            "all_metrics": all_metrics,
            "green_flags": [str(f) for f in flags['green_flags']],
            "red_flags": [str(f) for f in flags['red_flags']]
        }

        return jsonify(response_data), 201
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'message': f'Server processing error: {str(e)}'}), 500

@resume_bp.route('/analysis/<int:resume_id>', methods=['GET'])
@token_required
def get_analysis(current_user, resume_id):
    resume = ResumeModel.get_by_id(resume_id)
    if not resume:
        return jsonify({'message': 'Analysis not found'}), 404

    if resume['user_id'] != current_user['id'] and current_user['role'] != 'admin':
        return jsonify({'message': 'Unauthorized access to analysis'}), 403

    metrics = get_model_metrics()
    all_metrics = get_all_metrics()
    return jsonify({
        "id": resume['id'],
        "filename": resume['filename'],
        "prediction": {
            "predicted_role": resume['prediction'],
            "confidence": resume['confidence']
        },
        "model_performance": metrics,
        "all_metrics": all_metrics,
        "green_flags": resume['green_flags'],
        "red_flags": resume['red_flags'],
        "parsed_entities": resume['parsed_entities'],
        "created_at": resume['created_at']
    }), 200

@resume_bp.route('/history', methods=['GET'])
@token_required
def get_history(current_user):
    resumes = ResumeModel.get_by_user(current_user['id'])
    return jsonify({"resumes": resumes}), 200

@resume_bp.route('/skill-gap', methods=['POST'])
@token_required
def get_skill_gap(current_user):
    data = request.get_json() or {}
    skills = data.get('skills', [])
    target_role = data.get('target_role')
    
    if not target_role:
        return jsonify({'message': 'target_role is required'}), 400
        
    from services.skill_gap import analyze_skill_gap
    gap_analysis = analyze_skill_gap(skills, target_role)
    
    return jsonify({
        "status": "success",
        "skills": skills,
        "gap_analysis": gap_analysis
    }), 200

