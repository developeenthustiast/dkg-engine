@echo off
echo Starting TruthGraph Backend API Server...
echo.

echo Installing dependencies...
pip install -q aiohttp pydantic requests fastapi uvicorn websockets python-multipart substrate-interface cryptography

echo.
echo Starting server on http://localhost:8000
echo Press Ctrl+C to stop
echo.

cd backend
python main.py
