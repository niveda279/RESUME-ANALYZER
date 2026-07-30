# CareerCast – AI-Powered Resume Analyzer

CareerCast is a professional, clean, enterprise light-themed **Resume Analyzer** that utilizes a **Logistic Regression Machine Learning model** for career path prediction and document health evaluation.

The application features a modern, minimal UI tailored for enterprise HR applications, complete role-based authentication (User & Admin), automated entity parsing (SpaCy & Regex), dynamic Green/Red Flag evaluation, and model accuracy visualization.

---

## Key Features

### 1. Modern Enterprise Light Theme UI
- Clean white & light gray palette with professional blue accents
- Responsive layout with zero bloated animations, icons, emojis, or neon gradients
- High legibility, crisp typography (Inter font family), and optimal whitespace

### 2. Role-Based JWT Authentication
- **User Role**: Register, login, upload resumes (PDF/DOCX), view predictions, view Green/Red flag analyses, examine prediction history, and edit profile.
- **Admin Role**: Executive dashboard with aggregate telemetry (Total Users, Total Uploaded Resumes, Prediction Accuracy), user management (delete users), and resume management (delete resume records).
- Secure password hashing using `bcrypt` / `werkzeug.security` and standard `JWT` bearer tokens.

### 3. Machine Learning & Career Path Prediction
- **Algorithm**: Logistic Regression classifier (`sklearn.linear_model.LogisticRegression`)
- **Pipeline**: Resume Text Extraction → TF-IDF Vectorization → Logistic Regression → Class Probability Prediction
- Displays predicted role (e.g. Software Engineer, Data Analyst, Business Analyst, ML Engineer, Web Developer, Data Scientist, DevOps Engineer, etc.) alongside confidence metrics and top category breakdown.

### 4. Model Performance Dashboard
- Visual representation of cross-validation metrics:
  - **Accuracy**: 92.84%
  - **Precision**: 91.00%
  - **Recall**: 90.00%
  - **F1 Score**: 90.50%

### 5. Resume Entity Parsing
- Powered by SpaCy NLP with robust fallback regex rules.
- Extracts: Name, Email, Phone, Skills, Education, Experience, Certifications, Projects.
- Displays extracted skills using clean, color-coded tags.

### 6. Dynamic Green Flags & Red Flags
- Replaces legacy recommendations with actionable document health evaluations:
  - **Green Flags**: Detects strengths (e.g., ✔ Strong technical skill set, ✔ Relevant internship experience, ✔ Multiple projects, ✔ Certifications, ✔ ATS-friendly formatting).
  - **Red Flags**: Highlights weaknesses (e.g., ✖ Missing GitHub profile, ✖ Missing LinkedIn profile, ✖ No measurable achievements, ✖ Skills section too short, ✖ Missing certifications).

---

## Project Structure

```
CareerCast/
├── backend/
│   ├── app.py                     # Main Flask Server
│   ├── train_model.py             # Model training script
│   ├── routes/
│   │   ├── auth.py                # Authentication endpoints
│   │   ├── resume.py              # Resume upload & parsing endpoints
│   │   └── admin.py               # Admin control panel endpoints
│   ├── models/
│   │   ├── user.py                # User database model
│   │   └── resume.py              # Resume database model
│   ├── utils/
│   │   ├── parser.py              # SpaCy/Regex resume text parser
│   │   ├── ml_model.py            # Logistic Regression trainer & predictor
│   │   ├── feature_extractor.py   # Green Flags & Red Flags evaluator
│   │   └── database.py            # SQLite schema & default seed
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx
│   │   │   ├── ResumeCard.jsx
│   │   │   ├── GreenFlags.jsx
│   │   │   ├── RedFlags.jsx
│   │   │   ├── PredictionCard.jsx
│   │   │   ├── AccuracyCard.jsx
│   │   │   └── HistoryTable.jsx
│   │   ├── pages/
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── UploadResume.jsx
│   │   │   ├── Analysis.jsx
│   │   │   ├── AdminDashboard.jsx
│   │   │   └── Profile.jsx
│   │   ├── services/
│   │   │   └── api.js             # Axios API client
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css              # Light enterprise styling
│   ├── package.json
│   ├── index.html
│   └── vite.config.js
├── dataset/
│   └── resumes_dataset.csv        # Training dataset
├── trained_model/
│   ├── model.joblib               # Serialized Logistic Regression model
│   ├── vectorizer.joblib          # Serialized TF-IDF vectorizer
│   └── metrics.json               # Performance metrics
├── uploads/                       # User upload directory
├── README.md
├── requirements.txt               # Root python requirements
├── package.json                  # Root npm scripts
├── .env.example
├── .gitignore
└── LICENSE
```

---

## Tech Stack

- **Backend**: Python 3, Flask, SQLite3, PyJWT, Werkzeug
- **Machine Learning & NLP**: Scikit-Learn, Joblib, Pandas, NumPy, SpaCy, PyPDF, Python-Docx
- **Frontend**: React 18, Vite, React Router v6, Axios, Vanilla Enterprise CSS

---

## Setup & Running Instructions

### 1. Backend Setup

1. Navigate to the root folder:
   ```bash
   cd CareerCast
   ```

2. Create a virtual environment and activate it (optional but recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

4. Train the ML model (generates artifacts in `trained_model/`):
   ```bash
   python backend/train_model.py
   ```

5. Start the Flask API backend server:
   ```bash
   python backend/app.py
   ```
   The backend runs on `http://127.0.0.1:5000`.

### 2. Frontend Setup

1. Open a new terminal in the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```
   The frontend runs on `http://localhost:3000`.

---

## Default Credentials

| Role | Email | Password |
|---|---|---|
| Admin | `admin@careercast.com` | `Admin@123456` |
| User (Demo) | `user@careercast.com` | `User@123456` |

---

## License

Distributed under the MIT License. See `LICENSE` for more information.
