import React, { useState } from 'react';
import './FarePredictor.css';

function FarePredictor() {
  const jsDay = new Date().getDay(); // JS: Sunday=0..Saturday=6
  const pandasDay = (jsDay + 6) % 7; // Pandas dayofweek: Monday=0..Sunday=6
  const datasetYears = [2009, 2010, 2011, 2012, 2013, 2014, 2015];
  const defaultYear = datasetYears.includes(new Date().getFullYear())
    ? new Date().getFullYear()
    : 2015;

  const [formData, setFormData] = useState({
    distance_km: '',
    passenger_count: 1,
    hour: 12,
    month: new Date().getMonth() + 1,
    day_of_week: pandasDay,
    year: defaultYear,
    is_weekend: pandasDay >= 5 ? 1 : 0
  });

  const [predictionUsd, setPredictionUsd] = useState(null);
  const [predictionLkr, setPredictionLkr] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value, type } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'number' ? parseFloat(value) : value
    });
  };

  const handleDayChange = (e) => {
    const day = parseInt(e.target.value);
    setFormData(prev => ({
      ...prev,
      day_of_week: day,
      is_weekend: day >= 5 ? 1 : 0
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setPredictionUsd(null);
    setPredictionLkr(null);

    try {
      const response = await fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
      });

      if (!response.ok) {
        throw new Error('Failed to get prediction');
      }

      const data = await response.json();
      setPredictionUsd(data.predicted_fare_usd ?? data.predicted_fare ?? null);
      setPredictionLkr(data.predicted_fare_lkr ?? null);
    } catch (err) {
      setError(err.message || 'An error occurred while predicting');
    } finally {
      setLoading(false);
    }
  };

  const dayNames = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];
  const monthNames = ['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December'];

  return (
    <div className="predictor-container">
      <div className="card">
        <h1>🚕 Uber Fare Predictor</h1>
        
        <form onSubmit={handleSubmit} className="form">
          <div className="form-group">
            <label htmlFor="distance_km">Distance (km) *</label>
            <input
              type="number"
              id="distance_km"
              name="distance_km"
              value={formData.distance_km}
              onChange={handleInputChange}
              step="0.1"
              min="0"
              placeholder="Enter distance in kilometers"
              required
            />
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="passenger_count">Passengers *</label>
              <select
                id="passenger_count"
                name="passenger_count"
                value={formData.passenger_count}
                onChange={handleInputChange}
              >
                {[1, 2, 3, 4, 5, 6].map(num => (
                  <option key={num} value={num}>
                    {num} {num === 1 ? 'Passenger' : 'Passengers'}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="hour">Hour of Day *</label>
              <select
                id="hour"
                name="hour"
                value={formData.hour}
                onChange={handleInputChange}
              >
                {Array.from({ length: 24 }, (_, i) => (
                  <option key={i} value={i}>
                    {i.toString().padStart(2, '0')}:00
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="day_of_week">Day of Week *</label>
              <select
                id="day_of_week"
                name="day_of_week"
                value={formData.day_of_week}
                onChange={handleDayChange}
              >
                {dayNames.map((day, index) => (
                  <option key={index} value={index}>
                    {day}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label htmlFor="month">Month *</label>
              <select
                id="month"
                name="month"
                value={formData.month}
                onChange={handleInputChange}
              >
                {monthNames.map((month, index) => (
                  <option key={index} value={index + 1}>
                    {month}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="year">Year *</label>
              <select
                id="year"
                name="year"
                value={formData.year}
                onChange={handleInputChange}
              >
                {datasetYears.map(year => (
                  <option key={year} value={year}>
                    {year}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Weekend</label>
              <div className="weekend-display">
                {formData.is_weekend ? ' Yes' : '📅 No'}
              </div>
            </div>
          </div>

          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? 'Predicting...' : 'Predict Fare'}
          </button>
        </form>

        {error && (
          <div className="error" role="alert">
            <span>❌ Error: {error}</span>
          </div>
        )}

        {predictionUsd !== null && (
          <div className="result" role="status">
            <h2>Predicted Fare</h2>
            <div className="fare-amount">USD ${predictionUsd.toFixed(2)}</div>
            {predictionLkr !== null && (
              <div className="fare-amount">LKR {predictionLkr.toFixed(2)}</div>
            )}
            <p className="result-details">
              For a {formData.distance_km}km ride with {formData.passenger_count} 
              passenger{formData.passenger_count > 1 ? 's' : ''} on {dayNames[formData.day_of_week]} 
              at {formData.hour.toString().padStart(2, '0')}:00
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default FarePredictor;
