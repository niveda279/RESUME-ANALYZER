# CareerCast API Reference

> **Base URLs**
> - Flask API:   `http://localhost:5000/api`
> - FastAPI v2:  `http://localhost:5000/api/v2`
> - Swagger UI:  `http://localhost:5000/docs`

---

## Authentication

All resume endpoints are JWT-protected. Obtain a token via `/api/login` and pass it as:
```
Authorization: Bearer <token>
```

---

## Flask API Endpoints

### POST `/api/register`
Register a new user account.

**Request body** (JSON):
```json
{ "email": "user@example.com", "password": "SecurePass123" }
```

**Response 201:**
```json
{ "message": "User registered successfully" }
```

---

### POST `/api/login`
Authenticate and obtain a JWT token.

**Request body** (JSON):
```json
{ "email": "user@example.com", "password": "SecurePass123" }
```

**Response 200:**
```json
{
  "token": "<jwt>",
  "user": { "id": 1, "email": "user@example.com", "role": "user" }
}
```

**Error 401** — wrong credentials.

---

### POST `/api/upload` 🔒
Upload a resume file for parsing and ML prediction.

**Headers:** `Authorization: Bearer <token>`  
**Body:** `multipart/form-data` with field `file` (PDF / DOCX / TXT, max 10 MB).

**Response 201:**
```json
{
  "id": 42,
  "filename": "resume.pdf",
  "parsed_entities": {
    "name": "Jane Smith",
    "email": "jane@example.com",
    "phone": "555-0100",
    "skills": ["Python", "SQL", "Machine Learning"],
    "education": "M.S. Computer Science",
    "experience": "...",
    "certifications": "AWS Certified",
    "projects": "..."
  },
  "prediction": {
    "predicted_role": "Data Scientist",
    "confidence": 87.4,
    "breakdown": [
      { "role": "Data Scientist", "probability": 87.4 },
      { "role": "ML Engineer",   "probability": 9.1 }
    ]
  },
  "all_predictions": {
    "logistic_regression": { "predicted_role": "...", "confidence": 85.0, "breakdown": [...] },
    "random_forest":       { "predicted_role": "...", "confidence": 91.2, "breakdown": [...] },
    "xgboost":             { "predicted_role": "...", "confidence": 88.7, "breakdown": [...] },
    "best_model":          "Random Forest",
    "best_model_key":      "random_forest"
  },
  "model_performance": { "accuracy": 0.94, "f1_weighted": 0.93 },
  "green_flags": ["✔ Professional contact information", "..."],
  "red_flags":   ["✖ Missing LinkedIn profile", "..."]
}
```

**Errors:** `400` no file, `422` parse failure, `500` server error.

---

### GET `/api/analysis/<resume_id>` 🔒
Retrieve a saved analysis by ID.

**Response 200** — same structure as the upload response.  
**Error 404** — not found. **Error 403** — unauthorized.

---

### GET `/api/history` 🔒
List all resume analyses for the authenticated user.

**Response 200:**
```json
{ "resumes": [ { "id": 1, "filename": "...", "prediction": "...", ... } ] }
```

---

### POST `/api/skill-gap` 🔒
Analyse skills gap without uploading a file.

**Request body:**
```json
{
  "skills":      ["Python", "SQL", "Docker"],
  "target_role": "DevOps Engineer"
}
```

**Response 200:**
```json
{
  "status": "success",
  "skills": [...],
  "gap_analysis": {
    "predicted_role": "DevOps Engineer",
    "match_percentage": 42.86,
    "matched_skills": [{ "skill": "Python", "priority": "Moderate" }],
    "missing_skills": [{ "skill": "Kubernetes", "priority": "High" }],
    "priority_gaps": [{
      "skill": "Kubernetes",
      "priority": "High",
      "suggestion": "Set up a local Minikube cluster..."
    }]
  }
}
```

**Error 400** — `target_role` is required.

---

### GET `/api/health`
Public health check.

**Response 200:**
```json
{
  "status": "healthy",
  "service": "CareerCast API",
  "models": ["Logistic Regression", "Random Forest", "XGBoost"],
  "best_model": "Random Forest"
}
```

---

### GET `/api/ml-comparison`
Public endpoint returning all three model metrics.

**Response 200:**
```json
{
  "logistic_regression": { "accuracy": 0.94, "f1_weighted": 0.93, ... },
  "random_forest":       { "accuracy": 0.98, "f1_weighted": 0.97, ... },
  "xgboost":             { "accuracy": 0.96, "f1_weighted": 0.95, ... },
  "best_model":          "Random Forest",
  "best_model_key":      "random_forest"
}
```

---

## FastAPI v2 Endpoints

FastAPI v2 is mounted on the same server. Interactive docs: `http://localhost:5000/docs`

### GET `/api/v2/health`
```json
{ "status": "healthy", "service": "FastAPI CareerCast Service v2" }
```

### POST `/api/v2/predict`
Accept either a file upload or a raw text form field.

| Field       | Type   | Description              |
|-------------|--------|--------------------------|
| `file`      | File   | Resume file (multipart)  |
| `raw_text`  | string | Plain resume text (form) |

**Response 200:**
```json
{ "status": "success", "parsed_data": { ... }, "prediction": { ... } }
```

### POST `/api/v2/skill-gap`
**Request body (JSON):**
```json
{ "raw_text": "...", "target_role": "Data Scientist" }
```
`target_role` is optional — inferred from ML prediction if omitted.

**Response 200:**
```json
{ "status": "success", "candidate_skills": [...], "gap_analysis": { ... } }
```

### POST `/api/v2/recommendation`
Returns predictions from all three models.

**Request body (JSON):**
```json
{ "raw_text": "..." }
```

**Response 200:**
```json
{ "status": "success", "recommendations": { "logistic_regression": { ... }, ... } }
```

---

## Admin Endpoints 🔒 *(Admin role required)*

| Method | Path              | Description             |
|--------|-------------------|-------------------------|
| GET    | `/api/admin/users`   | List all users          |
| GET    | `/api/admin/resumes` | List all resume records |

---

## Error Reference

| Code | Meaning                                |
|------|----------------------------------------|
| 400  | Bad request / missing field            |
| 401  | Missing or invalid token               |
| 403  | Insufficient permissions               |
| 404  | Resource not found                     |
| 413  | File exceeds 10 MB limit               |
| 422  | Could not parse file content           |
| 500  | Internal server error                  |
