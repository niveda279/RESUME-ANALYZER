# CareerCast - Start Backend Server
# Run this from the RESUME-ANALYZER root directory

Write-Host "Starting CareerCast Flask Backend..." -ForegroundColor Cyan

# Install Python dependencies if needed
Write-Host "Checking Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet

# Start Flask backend
Write-Host "Starting Flask on http://127.0.0.1:5000 ..." -ForegroundColor Green
$env:FLASK_ENV = "development"
python backend/app.py
