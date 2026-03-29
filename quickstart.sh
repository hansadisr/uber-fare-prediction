#!/bin/bash
# Quick Start Script - Complete Setup for Uber Fare Prediction

echo "🚕 Uber Fare Prediction - Setup Script"
echo "========================================"

# Check if uber.csv exists
if [ ! -f "backend/uber.csv" ]; then
    echo "❌ Error: backend/uber.csv not found"
    echo "Please place your uber.csv file in the backend folder first"
    exit 1
fi

echo ""
echo "Step 1: Setting up Python Backend..."
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train model
echo ""
echo "Step 2: Training ML Model..."
python train_and_save_model.py

if [ ! -f "model.pkl" ]; then
    echo "❌ Model training failed"
    exit 1
fi

echo "✅ Model trained successfully"

# Start Flask in background
echo ""
echo "Step 3: Starting Flask API..."
python app.py &
FLASK_PID=$!
echo "Flask running (PID: $FLASK_PID)"

# Setup Frontend
cd ../frontend
echo ""
echo "Step 4: Setting up React Frontend..."
npm install

# Start React frontend
echo ""
echo "Step 5: Starting React App..."
npm run dev

# Cleanup on exit
trap "kill $FLASK_PID" EXIT

echo ""
echo "✅ Setup complete!"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:5000"
