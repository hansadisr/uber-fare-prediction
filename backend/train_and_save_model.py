"""
Script to train the Random Forest model and save it as pickle file
Run this after you have your uber.csv dataset
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split, KFold, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """Calculate distance between two geographic points"""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2*asin(sqrt(a))
    r = 6371
    return c*r

def preprocess_data(df):
    """Preprocess the data"""
    # Remove missing values
    df = df.dropna()
    
    # Filter unrealistic values
    df = df[
        (df['fare_amount'] > 0) & (df['fare_amount'] <= 200) &
        (df['passenger_count'] > 0) & (df['passenger_count'] <= 6)
    ]
    
    # Filter NYC coordinates
    df = df[
        (df['pickup_latitude'] >= 40.5) & (df['pickup_latitude'] <= 40.9) &
        (df['dropoff_latitude'] >= 40.5) & (df['dropoff_latitude'] <= 40.9) &
        (df['pickup_longitude'] >= -74.25) & (df['pickup_longitude'] <= -73.7) &
        (df['dropoff_longitude'] >= -74.25) & (df['dropoff_longitude'] <= -73.7)
    ]
    
    # Convert datetime
    df['pickup_datetime'] = pd.to_datetime(df['pickup_datetime'])
    
    # Feature engineering
    df['hour'] = df['pickup_datetime'].dt.hour
    df['day'] = df['pickup_datetime'].dt.day
    df['month'] = df['pickup_datetime'].dt.month
    df['day_of_week'] = df['pickup_datetime'].dt.dayofweek
    df['year'] = df['pickup_datetime'].dt.year
    df['is_weekend'] = (df['pickup_datetime'].dt.dayofweek >= 5).astype(int)
    
    # Calculate distance
    df['distance_km'] = df.apply(lambda row: haversine(
        row['pickup_longitude'],
        row['pickup_latitude'],
        row['dropoff_longitude'],
        row['dropoff_latitude']
    ), axis=1)
    
    return df

def train_model(df):
    """Train Random Forest model"""
    # Feature selection
    X = df[['distance_km', 'passenger_count', 'hour', 'month', 'day_of_week', 'year', 'is_weekend']]
    y = df['fare_amount']
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Hyperparameter tuning
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    
    rf_param_grid = {
        'n_estimators': [50, 100, 150],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2]
    }
    
    rf_search = RandomizedSearchCV(
        estimator=RandomForestRegressor(random_state=42, n_jobs=1),
        param_distributions=rf_param_grid,
        n_iter=4,
        cv=cv,
        scoring='neg_root_mean_squared_error',
        random_state=42,
        n_jobs=-1
    )
    
    print("Training Random Forest model...")
    rf_search.fit(X_train, y_train)
    
    best_model = rf_search.best_estimator_
    
    # Evaluate
    y_pred = best_model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)
    
    print(f"Best parameters: {rf_search.best_params_}")
    print(f"Test RMSE: {rmse:.2f}")
    print(f"Test R² Score: {r2:.4f}")
    
    return best_model

def main():
    # Load dataset
    print("Loading dataset...")
    df = pd.read_csv('uber.csv')
    print(f"Dataset shape: {df.shape}")
    
    # Preprocess
    print("Preprocessing data...")
    df = preprocess_data(df)
    print(f"Processed dataset shape: {df.shape}")
    
    # Train model
    print("Training model...")
    model = train_model(df)
    
    # Save model
    print("Saving model...")
    with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
    print("Model saved as model.pkl")

if __name__ == '__main__':
    main()
