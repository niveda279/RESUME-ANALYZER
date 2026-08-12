# CareerCast - Start Frontend Dev Server
# Run this from the RESUME-ANALYZER root directory in a SEPARATE terminal

Write-Host "Starting CareerCast React Frontend..." -ForegroundColor Cyan

# Install npm dependencies if needed
Write-Host "Checking npm dependencies..." -ForegroundColor Yellow
npm --prefix frontend install --silent

# Start Vite dev server
Write-Host "Starting Vite on http://localhost:3000 ..." -ForegroundColor Green
npm --prefix frontend run dev
