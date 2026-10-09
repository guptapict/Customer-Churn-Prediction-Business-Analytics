import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [overview, setOverview] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [formData, setFormData] = useState({
    gender: 'Female',
    SeniorCitizen: 'No',
    Partner: 'Yes',
    Dependents: 'No',
    tenure: 12,
    PhoneService: 'Yes',
    MultipleLines: 'No',
    InternetService: 'Fiber optic',
    OnlineSecurity: 'No',
    OnlineBackup: 'Yes',
    DeviceProtection: 'No',
    TechSupport: 'No',
    StreamingTV: 'No',
    StreamingMovies: 'No',
    Contract: 'Month-to-month',
    PaperlessBilling: 'Yes',
    PaymentMethod: 'Electronic check',
    MonthlyCharges: 70.0,
    TotalCharges: 840.0
  });

  useEffect(() => {
    fetch('http://localhost:8000/api/overview')
      .then(res => res.json())
      .then(data => setOverview(data))
      .catch(err => console.error("Error fetching overview", err));
  }, []);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: (name === 'tenure' || name === 'MonthlyCharges' || name === 'TotalCharges') ? Number(value) : value
    });
  };

  const handlePredict = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
      });
      const data = await response.json();
      setPrediction(data);
    } catch (err) {
      console.error("Prediction error", err);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>📉 Customer Churn Analytics & Prediction</h1>
      </header>
      
      <section className="overview-section">
        <h2>Executive Overview</h2>
        {overview ? (
          <div className="kpi-grid">
            <div className="kpi-card">
              <h3>Total Customers</h3>
              <p className="kpi-value">{overview.total_customers.toLocaleString()}</p>
            </div>
            <div className="kpi-card">
              <h3>Churned</h3>
              <p className="kpi-value">{overview.total_churned.toLocaleString()}</p>
            </div>
            <div className="kpi-card">
              <h3>Churn Rate</h3>
              <p className="kpi-value">{overview.churn_rate_percentage}%</p>
            </div>
            <div className="kpi-card">
              <h3>Avg Monthly Charges</h3>
              <p className="kpi-value">${overview.avg_monthly_charges}</p>
            </div>
          </div>
        ) : (
          <p>Loading overview...</p>
        )}
      </section>

      <section className="predict-section">
        <h2>Customer Risk Predictor</h2>
        <div className="predict-container">
          <form className="predict-form" onSubmit={handlePredict}>
            <div className="form-grid">
              <div className="form-group">
                <label>Tenure (Months)</label>
                <input type="number" name="tenure" value={formData.tenure} onChange={handleInputChange} />
              </div>
              <div className="form-group">
                <label>Monthly Charges ($)</label>
                <input type="number" step="0.1" name="MonthlyCharges" value={formData.MonthlyCharges} onChange={handleInputChange} />
              </div>
              <div className="form-group">
                <label>Contract</label>
                <select name="Contract" value={formData.Contract} onChange={handleInputChange}>
                  <option>Month-to-month</option>
                  <option>One year</option>
                  <option>Two year</option>
                </select>
              </div>
              <div className="form-group">
                <label>Payment Method</label>
                <select name="PaymentMethod" value={formData.PaymentMethod} onChange={handleInputChange}>
                  <option>Electronic check</option>
                  <option>Mailed check</option>
                  <option>Bank transfer (automatic)</option>
                  <option>Credit card (automatic)</option>
                </select>
              </div>
            </div>
            <button type="submit" className="predict-btn">Predict Churn Risk</button>
          </form>

          {prediction && (
            <div className={`result-card ${prediction.risk_category.replace(" ", "-").toLowerCase()}`}>
              <h3>Prediction Result</h3>
              <div className="result-metric">
                <span className="prob">{prediction.probability_percentage}%</span>
                <span className="risk">{prediction.risk_category}</span>
              </div>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}

export default App;
