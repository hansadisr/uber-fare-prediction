# 🚕 Uber Fare Prediction System

A full-stack Machine Learning application with a React UI that predicts Uber fares using a Random Forest model served by a Flask API.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    React UI (Frontend)                      │
│              http://localhost:3000                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                    HTTP Request
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Python Flask API                           │
│              http://localhost:5000                          │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│            Random Forest ML Model (Scikit-learn)            │
│         Predicts fare based on trip features               │
└─────────────────────────────────────────────────────────────┘
```

## Features

- **React Frontend**: Modern, responsive UI for fare predictions
- **Flask Backend**: RESTful API to serve predictions
- **Random Forest Model**: Trained on NYC Uber trip data
- **Real-time Predictions**: Instant fare estimates based on:
  - Distance (km)
  - Passenger count
  - Time of day (hour)
  - Day of week & month
  - Year
  - Weekend flag

## Project Structure

```
UberFarePrediction/
├── backend/
│   ├── app.py                       # Flask API application
│   ├── train_and_save_model.py     # Model training script
│   ├── model.pkl                    # Trained model (generated)
│   └── requirements.txt             # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── FarePredictor.jsx   # Main predictor component
│   │   │   └── FarePredictor.css   # Styling
│   │   ├── App.jsx                 # Main app component
│   │   ├── App.css                 # App styling
│   │   └── main.jsx                # Entry point
│   ├── index.html                  # HTML template
│   ├── package.json                # Frontend dependencies
│   └── vite.config.js              # Vite configuration
└── README.md                        # This file
```

## Prerequisites

- **Python 3.8+** installed on your system
- **Node.js 16+** and npm installed
- **Your uber.csv dataset** (place in the backend folder)

## Setup Instructions

### Step 1: Train & Save the Model

1. Navigate to the backend folder:
   ```bash
   cd UberFarePrediction/backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Place your `uber.csv` file in the `backend` folder

4. Train the model and save it:
   ```bash
   python train_and_save_model.py
   ```
   
   This will:
   - Load and preprocess your data
   - Train a Random Forest model with hyperparameter tuning
   - Save it as `model.pkl`

### Step 2: Start the Flask API

1. In the `backend` folder, run:
   ```bash
   python app.py
   ```
   
   You should see:
   ```
   WARNING in app.run() is not recommended for production use.
   Running on http://127.0.0.1:5000
   ```

2. Test the API:
   ```bash
   curl http://localhost:5000/health
   ```

### Step 3: Start the React Frontend

1. In a new terminal, navigate to the frontend folder:
   ```bash
   cd UberFarePrediction/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```
   
   The UI will open at `http://localhost:3000`

## Usage

1. **Enter Trip Details**:
   - Distance in kilometers
   - Number of passengers
   - Time of day (hour)
   - Day of week and month
   - Year

2. **Get Prediction**: Click "Predict Fare" button

3. **View Result**: The predicted fare will display with trip summary

## API Endpoints

### Health Check
```
GET /health
Response: { "status": "healthy", "model_loaded": true }
```

### Predict Fare
```
POST /predict
Content-Type: application/json

Request Body:
{
  "distance_km": 5.2,
  "passenger_count": 2,
  "hour": 14,
  "month": 3,
  "day_of_week": 2,
  "year": 2024,
  "is_weekend": 0
}

Response:
{
  "predicted_fare": 18.50,
  "input_features": { ... }
}
```

### Model Info
```
GET /model-info
Response: { "model_type": "Random Forest Regressor", "features": [...] }
```

## Troubleshooting

### Model Not Found
- **Error**: "Model not loaded"
- **Solution**: Run `train_and_save_model.py` first to create `model.pkl`

### CORS Error
- **Error**: "Access to XMLHttpRequest blocked by CORS policy"
- **Solution**: Flask-CORS is configured. Ensure Flask app is running on port 5000

### Port Already in Use
- **Flask**: Change port in `app.py` line `app.run(debug=True, port=5000)`
- **React**: Change port in `vite.config.js` line `port: 3000`

### Connection Refused
- **Ensure both terminals are open**: One for backend, one for frontend
- **Check localhost**: Verify apps are running on correct ports

## Interview Talking Points

### Architecture & Design
- **Separation of Concerns**: Frontend handles UI/UX, backend handles ML predictions
- **Scalability**: Flask API can handle multiple concurrent predictions
- **REST API**: Standard HTTP protocol for communication

### Data Pipeline
- **Feature Engineering**: Extracted temporal features (hour, day, month, weekend)
- **Distance Calculation**: Used Haversine formula for geographic distance
- **Data Cleaning**: Removed outliers and NYC coordinate validation

### Model Selection
- **Random Forest vs Linear Regression**: Random Forest captured non-linear fare patterns
- **Hyperparameter Tuning**: Used RandomizedSearchCV for optimal model parameters
- **Cross-Validation**: 5-fold CV to ensure model generalization

### Key Metrics
- **RMSE**: Measures average prediction error in fare amounts
- **R² Score**: Indicates model explains X% of fare variance
- **Trade-off**: Model complexity vs prediction accuracy

### Challenges & Solutions
- **Challenge**: Outlier fares affecting model training
  - **Solution**: Filtered unrealistic fare amounts and coordinates
- **Challenge**: Temporal features need proper encoding
  - **Solution**: Extracted day of week and weekend flag from timestamp
- **Challenge**: API latency for real-time predictions
  - **Solution**: Model loaded in memory, predictions under 100ms

## Future Enhancements

- [ ] Add location autocomplete for pickup/dropoff
- [ ] Real-time pricing trends
- [ ] Historical fare comparison
- [ ] Prediction confidence intervals
- [ ] User activity logging
- [ ] Docker containerization for deployment
- [ ] Authentication and rate limiting
- [ ] Batch prediction support

## Dependencies

### Backend
- Flask 2.3.0
- scikit-learn 1.2.0
- pandas 2.0.0
- numpy 1.24.0
- Flask-CORS 4.0.0

### Frontend
- React 18.2.0
- React-DOM 18.2.0
- Vite 4.3.0

## License

This project is open source and available for educational purposes.

## Contact & Support

For issues or questions, please refer to the project documentation or reach out with specific error messages.

---

**Happy predicting! 🎉**
