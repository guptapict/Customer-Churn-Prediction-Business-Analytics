from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib
import os
import sqlite3

app = FastAPI(title="Customer Churn Prediction API")

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'churn_model.pkl')
DB_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'churn_db.sqlite')

# Load the model on startup
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Warning: Could not load model: {e}")

class CustomerData(BaseModel):
    gender: str
    SeniorCitizen: str
    Partner: str
    Dependents: str
    tenure: int
    PhoneService: str
    MultipleLines: str
    InternetService: str
    OnlineSecurity: str
    OnlineBackup: str
    DeviceProtection: str
    TechSupport: str
    StreamingTV: str
    StreamingMovies: str
    Contract: str
    PaperlessBilling: str
    PaymentMethod: str
    MonthlyCharges: float
    TotalCharges: float

@app.get("/")
def root():
    return {"message": "Customer Churn Prediction API is running"}

@app.post("/predict")
def predict_churn(customer: CustomerData):
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded on the server.")
        
    input_df = pd.DataFrame([customer.dict()])
    try:
        prob = model.predict_proba(input_df)[0][1]
        
        if prob >= 0.70:
            risk = "High Risk"
        elif prob >= 0.40:
            risk = "Medium Risk"
        else:
            risk = "Low Risk"
            
        return {
            "probability": prob,
            "probability_percentage": round(prob * 100, 1),
            "risk_category": risk
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/overview")
def get_overview():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM customers")
        total_customers = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM customers WHERE Churn = 'Yes'")
        total_churned = cursor.fetchone()[0]
        
        cursor.execute("SELECT AVG(MonthlyCharges) FROM customers")
        avg_monthly = cursor.fetchone()[0]
        
        conn.close()
        
        churn_rate = total_churned / total_customers if total_customers > 0 else 0
        
        return {
            "total_customers": total_customers,
            "total_churned": total_churned,
            "churn_rate_percentage": round(churn_rate * 100, 1),
            "avg_monthly_charges": round(avg_monthly, 2)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/data")
def get_all_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query("SELECT * FROM customers", conn)
        conn.close()
        return df.to_dict(orient="records")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
