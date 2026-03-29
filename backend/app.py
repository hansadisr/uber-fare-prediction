from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import os

app = Flask(__name__)
CORS(app)

# Approximate conversion rate; update this value when needed.
USD_TO_LKR_RATE = 325.0

# Load the trained Random Forest model
model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')

def load_model():
    """Load the trained Random Forest model"""
    try:
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        print("Model file not found. Please train and save the model first.")
        return None

# Load model on startup
model = load_model()

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'model_loaded': model is not None})

@app.route('/predict', methods=['POST'])
def predict():
    """
    Predict fare amount based on input features
    Expected JSON:
    {
        "distance_km": float,
        "passenger_count": int,
        "hour": int,
        "month": int,
        "day_of_week": int,
        "year": int,
        "is_weekend": int
    }
    """
    try:
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        data = request.get_json()
        
        # Validate input
        required_fields = ['distance_km', 'passenger_count', 'hour', 'month', 'day_of_week', 'year', 'is_weekend']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing field: {field}'}), 400
        
        # Extract features in the correct order
        features = np.array([[
            float(data['distance_km']),
            int(data['passenger_count']),
            int(data['hour']),
            int(data['month']),
            int(data['day_of_week']),
            int(data['year']),
            int(data['is_weekend'])
        ]])
        
        # Make prediction
        prediction = model.predict(features)[0]
        predicted_fare_usd = round(float(prediction), 2)
        predicted_fare_lkr = round(predicted_fare_usd * USD_TO_LKR_RATE, 2)
        
        return jsonify({
            'predicted_fare': predicted_fare_usd,
            'predicted_fare_usd': predicted_fare_usd,
            'predicted_fare_lkr': predicted_fare_lkr,
            'exchange_rate_lkr_per_usd': USD_TO_LKR_RATE,
            'input_features': data
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/model-info', methods=['GET'])
def model_info():
    """Return information about the model"""
    return jsonify({
        'model_type': 'Random Forest Regressor',
        'features': ['distance_km', 'passenger_count', 'hour', 'month', 'day_of_week', 'year', 'is_weekend']
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
