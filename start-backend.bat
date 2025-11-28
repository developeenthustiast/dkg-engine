@echo off
echo Starting TruthGraph Backend API Server...
echo.

echo Installing dependencies...
cd ..
pip install -q -r requirements.txt
cd backend
pip install -q -r requirements.txt

echo.
echo Starting server on http://localhost:8000
echo Press Ctrl+C to stop
echo.

python main.py
