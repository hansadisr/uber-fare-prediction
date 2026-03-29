# Quick Start - Uber Fare Prediction
# Run this batch file for Windows

@echo off
echo 🚕 Uber Fare Prediction - Setup Script
echo ========================================

REM Check if uber.csv exists
if not exist "backend\uber.csv" (
    echo ❌ Error: backend\uber.csv not found
    echo Please place your uber.csv file in the backend folder first
    pause
    exit /b 1
)

echo.
echo Step 1: Setting up Python Backend...
cd backend

REM Create virtual environment
python -m venv venv
call venv\Scripts\activate.bat

REM Install dependencies
pip install -r requirements.txt

REM Train model
echo.
echo Step 2: Training ML Model...
python train_and_save_model.py

if not exist "model.pkl" (
    echo ❌ Model training failed
    pause
    exit /b 1
)

echo ✅ Model trained successfully

REM Start Flask
echo.
echo Step 3: Starting Flask API...
echo Launching Flask on http://localhost:5000
start cmd /k "python app.py"

REM Setup Frontend
cd ..\frontend
echo.
echo Step 4: Setting up React Frontend...
call npm install

REM Start React
echo.
echo Step 5: Starting React App...
echo Launching React on http://localhost:3000
call npm run dev

echo.
echo ✅ Setup complete!
echo Frontend: http://localhost:3000
echo Backend: http://localhost:5000
pause
