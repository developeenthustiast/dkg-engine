# TruthGraph Web Interface

## Setup

1. **Start the Backend API**:
```bash
cd backend
pip install -r requirements.txt
python main.py
```
The API will run on `http://localhost:8000`

2. **Start the Frontend**:
```bash
cd web
npm install
npm run dev
```
The web interface will run on `http://localhost:5173`

## Usage

1. Open `http://localhost:5173` in your browser
2. Enter a goal for the agent (e.g., "Check if 'The earth is flat' is a hallucination")
3. Click "Run Agent"
4. Watch the real-time thought process in the right panel
5. See the final result when the agent completes

## Features

- 🎨 **Modern UI**: Glass morphism with smooth animations
- 🔄 **Real-time Updates**: See agent thinking live
- 📊 **Visual Feedback**: Color-coded message types
- 🚀 **Fast**: Vite for instant HMR
- 💅 **Responsive**: Works on all screen sizes
