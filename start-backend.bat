@echo off
echo Starting TruthGraph Backend API Server...
echo.

cd backend
echo Installing dependencies...
pip install -q fastapi uvicorn websockets python-multipart

echo.
echo Starting server on http://localhost:8000
echo Press Ctrl+C to stop
echo.

python main.py
