# Deployment Guide

## Local Development

### Backend (FastAPI + Flask)

```bash
cd RESUME-ANALYZER
pip install -r backend/requirements.txt

# Train models if not already trained
python backend/train_model.py

# Start the combined FastAPI+Flask server
cd backend
uvicorn main:app --host 0.0.0.0 --port 5000 --reload
```

Backend is now available at:
- Flask API: `http://localhost:5000/api`
- FastAPI v2: `http://localhost:5000/api/v2`
- Swagger UI: `http://localhost:5000/docs`

### Frontend (React/Vite)

```bash
cd RESUME-ANALYZER/frontend
npm install
npm run dev
# → http://localhost:5173
```

### Streamlit Review UI

```bash
cd RESUME-ANALYZER
pip install reportlab streamlit
streamlit run streamlit/review_app.py
# → http://localhost:8501
```

---

## Environment Variables

Copy `.env.example` to `.env` and fill in values:

```bash
cp .env.example .env
```

| Variable               | Default                       | Description                        |
|------------------------|-------------------------------|------------------------------------|
| `SECRET_KEY`           | (hardcoded fallback)          | JWT signing secret — **change in prod** |
| `DATABASE_URL`         | `sqlite:///backend/careercast.db` | Database path                  |
| `MLFLOW_TRACKING_URI`  | (local)                       | MLflow server URI                  |
| `API_URL`              | `http://127.0.0.1:5000/api/v2` | For Streamlit app                 |
| `DB_PATH`              | `backend/careercast.db`       | For Streamlit cohort analytics     |

> [!WARNING]
> **Never commit a `.env` file with real secrets.** The `.env` file is git-ignored by default.

> [!CAUTION]
> The `SECRET_KEY` used for JWT signing in `routes/auth.py` should be set via the
> environment variable in production. The hardcoded fallback is for development only.

---

## Render Deployment (Full Stack)

The `render.yaml` file configures a Render Web Service running the combined
FastAPI+Flask backend with Gunicorn. The React frontend is served as static files
from `frontend/dist/`.

### Steps

1. Push code to GitHub.
2. Connect the repository to [Render](https://render.com).
3. Render will auto-detect `render.yaml` and deploy the service.
4. Set environment variables in the Render dashboard.
5. The first deploy will train models automatically via `train_model.py`.

**Procfile (for Render/Heroku):**
```
web: cd backend && gunicorn -w 2 -k uvicorn.workers.UvicornWorker main:app
```

---

## Vercel Deployment (Frontend)

The `vercel.json` file configures the React frontend for Vercel edge deployment.

```bash
cd frontend
npm run build
vercel deploy
```

Update `VITE_API_URL` in your Vercel environment variables to point to the Render backend.

---

## Docker (Manual)

A minimal Dockerfile for the backend:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY backend/ ./backend/
COPY dataset/ ./dataset/
RUN pip install --no-cache-dir -r backend/requirements.txt
RUN python backend/train_model.py
EXPOSE 5000
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "5000"]
```

---

## Pip Package Installation

```bash
cd RESUME-ANALYZER
pip install -e .
# or install backend extras
pip install -e ".[backend]"

# Verify CLI
careercast version
careercast models
```

---

## Production Checklist

- [ ] Set `SECRET_KEY` via environment variable (not hardcoded)
- [ ] Use PostgreSQL or another production database instead of SQLite
- [ ] Enable HTTPS (via Render/Vercel automatic TLS or custom certificate)
- [ ] Set `ALLOWED_ORIGINS` to specific frontend URL instead of `*`
- [ ] Retrain models on a larger, real-world dataset
- [ ] Configure MLflow remote tracking URI with access control
- [ ] Set up log aggregation (e.g. Datadog, Sentry)
