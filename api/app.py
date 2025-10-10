# api/app.py

import joblib
from pathlib import Path
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

# --- 1. DEFINE YOUR API ---
# Create an instance of the FastAPI class
app = FastAPI(title="Customer Churn Prediction API")

# --- 2. LOAD YOUR MODEL ---
# Define the path to your trained model
# Note: This path is relative to where you run `uvicorn` from (the project root)
model_path = Path('models/artifacts/churn_model_v1.joblib')
model = joblib.load(model_path)
print(f"Model loaded successfully from {model_path}")

# --- 3. DEFINE THE INPUT DATA MODEL ---
# Use Pydantic to define the structure and data types of your input
class CustomerFeatures(BaseModel):
    recency: int
    frequency: int
    monetary: float
    
    # Example to show in the API docs
    class Config:
        json_schema_extra = {
            "example": {
                "recency": 10,
                "frequency": 5,
                "monetary": 500.50
            }
        }

# --- 4. CREATE YOUR PREDICTION ENDPOINT ---
@app.post("/predict_churn")
def predict_churn(features: CustomerFeatures):
    """
    Receives customer features, predicts churn, and sends a Slack alert for high-risk VIPs.
    """
    # Convert the input features to a pandas DataFrame
    input_df = pd.DataFrame([features.model_dump()])
    
    # Make a prediction
    prediction_proba = model.predict_proba(input_df)[0][1] # Probability of class 1 (churn)
    
    # --- SLACK ALERT LOGIC ---
    # Alert if churn probability is high AND the customer is high-value (monetary > 1000)
    if prediction_proba > 0.75 and features.monetary > 1000:
        # IMPORTANT: Store your webhook URL securely, e.g., in an environment variable.
        # For this demo, we'll get it from an environment variable or use a placeholder.
        slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL", "YOUR_SLACK_WEBHOOK_URL_HERE")
        
        message = (
            f":warning: High-Risk VIP Customer Alert!\n"
            f"Churn Probability: *{prediction_proba:.2%}*\n"
            f"Recency: {features.recency} days\n"
            f"Frequency: {features.frequency} purchases\n"
            f"Monetary Value: ${features.monetary:,.2f}"
        )
        
        try:
            requests.post(slack_webhook_url, json={"text": message})
            print("Slack alert sent for high-risk customer.")
        except Exception as e:
            print(f"Error sending Slack alert: {e}")

    # Return the result
    return {
        "churn_probability": round(prediction_proba, 4)
    }

# --- 5. CREATE A ROOT ENDPOINT (Optional) ---
@app.get("/")
def read_root():
    return {"message": "Welcome to the Customer Churn Prediction API"}