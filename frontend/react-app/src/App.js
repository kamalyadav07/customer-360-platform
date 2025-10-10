// frontend/react-app/src/App.js

import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  // State variables to hold the form input values
  const [recency, setRecency] = useState(10);
  const [frequency, setFrequency] = useState(5);
  const [monetary, setMonetary] = useState(500);

  // State variables to hold the prediction result and loading status
  const [prediction, setPrediction] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handlePredict = async () => {
    setIsLoading(true);
    setPrediction(null); // Clear previous prediction

    const inputData = {
      recency: parseInt(recency),
      frequency: parseInt(frequency),
      monetary: parseFloat(monetary)
    };

    try {
      // Make sure your FastAPI server is running on http://127.0.0.1:8000
      const response = await axios.post('http://127.0.0.1:8000/predict_churn', inputData);
      setPrediction(response.data.churn_probability);
    } catch (error) {
      console.error("Error fetching prediction:", error);
      alert("Failed to get prediction. Is the backend server running?");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Customer Churn Prediction</h1>
        <div className="form">
          <div className="input-group">
            <label>Recency (days since last purchase)</label>
            <input type="number" value={recency} onChange={(e) => setRecency(e.target.value)} />
          </div>
          <div className="input-group">
            <label>Frequency (total number of purchases)</label>
            <input type="number" value={frequency} onChange={(e) => setFrequency(e.target.value)} />
          </div>
          <div className="input-group">
            <label>Monetary (total spend)</label>
            <input type="number" value={monetary} onChange={(e) => setMonetary(e.target.value)} />
          </div>
          <button onClick={handlePredict} disabled={isLoading}>
            {isLoading ? 'Predicting...' : 'Predict Churn'}
          </button>
        </div>
        {prediction !== null && (
          <div className="result">
            <h2>Churn Probability: {(prediction * 100).toFixed(2)}%</h2>
            <p>{prediction > 0.5 ? "This customer is likely to churn." : "This customer is likely to stay."}</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;