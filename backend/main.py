from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.wsgi import WSGIMiddleware
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
import os
import io

# Import the existing Flask app
from app import app as flask_app
from utils.parser import extract_text_from_file, parse_resume_text
from utils.ml_service import get_best_model_prediction, predict_all_models
from services.skill_gap import analyze_skill_gap

app = FastAPI(
    title="CareerCast API (Milestone 3)",
    description="FastAPI service serving Milestone 3 advanced endpoints while preserving the Flask app.",
    version="2.0.0",
)

# Enable CORS for the FastAPI endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Schemas
class PredictionRequest(BaseModel):
    raw_text: str

class RecommendationRequest(BaseModel):
    raw_text: str

class SkillGapRequest(BaseModel):
    raw_text: str
    target_role: Optional[str] = None

# Endpoints
@app.post("/api/v2/predict")
async def predict_resume(file: UploadFile = File(None), raw_text: Optional[str] = Form(None)):
    """Predict career probabilities based on resume text or file."""
    text = ""
    if file:
        try:
            content = await file.read()
            # Save temporarily to extract text (parser needs file path for pdf/docx)
            # A more robust approach writes to a temp directory.
            temp_path = f"/tmp/{file.filename}"
            # On Windows, use a standard temp dir
            temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "uploads", "temp")
            os.makedirs(temp_dir, exist_ok=True)
            temp_path = os.path.join(temp_dir, file.filename)
            
            with open(temp_path, "wb") as f:
                f.write(content)
                
            text = extract_text_from_file(temp_path)
            
            if os.path.exists(temp_path):
                os.remove(temp_path)
                
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error reading file: {str(e)}")
    elif raw_text:
        text = raw_text
    else:
        raise HTTPException(status_code=400, detail="Must provide either file or raw_text")
        
    if not text or text.startswith("Error"):
        raise HTTPException(status_code=400, detail="Could not extract text from document")

    parsed_data = parse_resume_text(text)
    prediction = get_best_model_prediction(text)
    
    return {
        "status": "success",
        "parsed_data": parsed_data,
        "prediction": prediction
    }

@app.post("/api/v2/skill-gap")
async def analyze_gap(request: SkillGapRequest):
    """Analyze skill gap between candidate skills and target role."""
    if not request.raw_text:
        raise HTTPException(status_code=400, detail="raw_text is required")
        
    parsed_data = parse_resume_text(request.raw_text)
    candidate_skills = parsed_data.get("skills", [])
    
    target_role = request.target_role
    if not target_role:
        # Infer from ML model
        prediction = get_best_model_prediction(request.raw_text)
        target_role = prediction.get("predicted_role", "Software Engineer")
        
    gap_analysis = analyze_skill_gap(candidate_skills, target_role)
    
    return {
        "status": "success",
        "candidate_skills": candidate_skills,
        "gap_analysis": gap_analysis
    }

@app.post("/api/v2/recommendation")
async def get_recommendation(request: RecommendationRequest):
    """Get all model predictions as recommendations."""
    if not request.raw_text:
        raise HTTPException(status_code=400, detail="raw_text is required")
        
    all_predictions = predict_all_models(request.raw_text)
    return {
        "status": "success",
        "recommendations": all_predictions
    }

@app.get("/api/v2/health")
async def health_check():
    return {"status": "healthy", "service": "FastAPI CareerCast Service v2"}

# Mount the Flask application to serve the existing `/api` and static files
app.mount("/", WSGIMiddleware(flask_app))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)
