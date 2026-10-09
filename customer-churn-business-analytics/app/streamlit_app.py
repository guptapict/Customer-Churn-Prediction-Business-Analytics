import streamlit as st
import pandas as pd
import joblib
import os
import sqlite3
import numpy as np

# Page config
st.set_page_config(page_title="Customer Churn Platform", page_icon="📈", layout="wide")

# Custom CSS for a professional, premium UI
st.markdown("""
<style>
    /* Main background and typography */
    .stApp {
        background-color: #f8fafc;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #0f172a;
        font-weight: 700 !important;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e2e8f0;
    }
    
    /* Style the main form container */
    [data-testid="stForm"] {
        background: white;
        border-radius: 16px;
        padding: 30px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #e2e8f0;
    }
    
    /* Style the submit button */
    [data-testid="stFormSubmitButton"] > button {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 15px;
    }
    
    [data-testid="stFormSubmitButton"] > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3);
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
    }

    /* Input fields styling */
    .stSelectbox div[data-baseweb="select"], 
    .stNumberInput div[data-baseweb="input"] {
        border-radius: 8px;
        border-color: #cbd5e1;
        background-color: #f1f5f9;
    }
    
    /* Metric cards */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
        color: #0f172a;
    }
    
    .prediction-card {
        background: white;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        border-left: 6px solid #3b82f6;
        margin-top: 20px;
    }
    
    /* Product Box styling */
    .product-box {
        background: white;
        padding: 24px;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #e2e8f0;
        height: 220px;
        margin-bottom: 15px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .product-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.1);
    }
    .product-box h3 {
        margin-top: 10px;
        margin-bottom: 8px;
        font-size: 1.25rem;
    }
    .product-box p {
        color: #64748b;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    .box-icon {
        font-size: 2.5rem;
    }
</style>
""", unsafe_allow_html=True)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@st.cache_data
def load_data():
    data_path = os.path.join(BASE_DIR, 'data', 'processed', 'cleaned_churn_data.csv')
    return pd.read_csv(data_path)

@st.cache_resource
def load_model():
    MODEL_PATH = os.path.join(BASE_DIR, 'models', 'churn_model.pkl')
    return joblib.load(MODEL_PATH)

try:
    df = load_data()
    model = load_model()
except Exception as e:
    st.error("Data or model not found. Please run the training pipeline first.")
    st.stop()

def home_page():
    st.markdown("<h1 style='text-align: center; color: #0f172a; margin-top: 2rem;'>Customer Churn Intelligence</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #475569; margin-bottom: 3rem;'>An end-to-end enterprise platform for predicting, analyzing, and preventing customer churn.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="product-box" style="border-top: 4px solid #3b82f6;">
            <div class="box-icon">📈</div>
            <h3>Executive Overview</h3>
            <p>High-level historical churn performance and key metrics at a glance.</p>
        </div>
        """, unsafe_allow_html=True)
        st.page_link(overview_page, label="View Overview", icon="📈")
            
    with col2:
        st.markdown("""
        <div class="product-box" style="border-top: 4px solid #10b981;">
            <div class="box-icon">📊</div>
            <h3>Customer Analytics</h3>
            <p>Filter and explore the historical dataset to uncover specific churn patterns.</p>
        </div>
        """, unsafe_allow_html=True)
        st.page_link(analytics_page, label="Explore Data", icon="📊")
            
    with col3:
        st.markdown("""
        <div class="product-box" style="border-top: 4px solid #f59e0b;">
            <div class="box-icon">💻</div>
            <h3>SQL Analytics</h3>
            <p>Direct querying of the database to extract deep business logic.</p>
        </div>
        """, unsafe_allow_html=True)
        st.page_link(sql_page, label="Run Queries", icon="💻")
            
    st.markdown("<br>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)
    
    with col4:
        st.markdown("""
        <div class="product-box" style="border-top: 4px solid #6366f1;">
            <div class="box-icon">⚙️</div>
            <h3>ML Model Performance</h3>
            <p>Evaluate the performance and metrics of our trained predictive models.</p>
        </div>
        """, unsafe_allow_html=True)
        st.page_link(ml_page, label="View Models", icon="⚙️")
            
    with col5:
        st.markdown("""
        <div class="product-box" style="border-top: 4px solid #ec4899;">
            <div class="box-icon">🎯</div>
            <h3>Churn Predictor</h3>
            <p>AI-powered tool to predict individual customer churn probability.</p>
        </div>
        """, unsafe_allow_html=True)
        st.page_link(predictor_page, label="Launch Predictor", icon="🎯")
            
    with col6:
        st.markdown("""
        <div class="product-box" style="border-top: 4px solid #8b5cf6;">
            <div class="box-icon">💡</div>
            <h3>Retention Strategy</h3>
            <p>Strategic action plans and personalized incentives to reduce churn.</p>
        </div>
        """, unsafe_allow_html=True)
        st.page_link(strategy_page, label="View Strategy", icon="💡")

def executive_overview():
    st.title("📈 Executive Overview")
    st.markdown("High-level historical churn performance.")
    
    total_customers = len(df)
    total_churned = len(df[df['Churn'] == 'Yes'])
    churn_rate = total_churned / total_customers
    avg_monthly = df['MonthlyCharges'].mean()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Customers", f"{total_customers:,}")
    col2.metric("Total Churned", f"{total_churned:,}")
    col3.metric("Churn Rate", f"{churn_rate:.1%}")
    col4.metric("Avg Monthly Charges", f"${avg_monthly:.2f}")
    
    st.divider()
    st.subheader("Historical Churn Insights")
    st.bar_chart(df.groupby('Contract')['Churn'].value_counts().unstack(), height=300)

def customer_analytics():
    st.title("📊 Customer Analytics & Segmentation")
    st.markdown("Filter the historical dataset to uncover specific churn patterns across different segments.")
    
    # Filters
    st.subheader("Filter Data")
    col1, col2, col3 = st.columns(3)
    with col1:
        contract_filter = st.multiselect("Contract Type", df['Contract'].unique(), default=df['Contract'].unique())
    with col2:
        payment_filter = st.multiselect("Payment Method", df['PaymentMethod'].unique(), default=df['PaymentMethod'].unique())
    with col3:
        internet_filter = st.multiselect("Internet Service", df['InternetService'].unique(), default=df['InternetService'].unique())
        
    # Apply filters
    filtered_df = df[
        (df['Contract'].isin(contract_filter)) &
        (df['PaymentMethod'].isin(payment_filter)) &
        (df['InternetService'].isin(internet_filter))
    ]
    
    st.markdown(f"**Showing {len(filtered_df):,} customers based on your filters.**")
    
    if len(filtered_df) > 0:
        colA, colB = st.columns(2)
        with colA:
            st.markdown("### Churn Distribution in Segment")
            churn_counts = filtered_df['Churn'].value_counts()
            st.bar_chart(churn_counts)
            
        with colB:
            st.markdown("### Churn by Tenure Group")
            # Group by TenureGroup and Churn
            tenure_churn = filtered_df.groupby(['TenureGroup', 'Churn']).size().unstack(fill_value=0)
            st.bar_chart(tenure_churn)
            
        st.markdown("### Monthly Charges Distribution")
        st.area_chart(filtered_df.groupby('MonthlyCharges').size())
    else:
        st.warning("No customers match the selected filters.")

def sql_analytics():
    st.title("💻 SQL Analytics")
    st.markdown("Direct querying of the SQLite database to extract business logic and aggregations.")
    
    DB_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'churn_db.sqlite')
    if not os.path.exists(DB_PATH):
        st.error("Database not found. Please run the data processing script.")
    else:
        conn = sqlite3.connect(DB_PATH)
        
        st.subheader("1. Churn Rate by Contract Type")
        q1 = '''
        SELECT 
            Contract,
            COUNT(customerID) AS TotalCustomers,
            SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS ChurnedCustomers,
            ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) / COUNT(customerID) * 100, 2) AS ChurnRatePercentage
        FROM customers
        GROUP BY Contract
        ORDER BY ChurnRatePercentage DESC;
        '''
        st.code(q1, language='sql')
        df_q1 = pd.read_sql_query(q1, conn)
        st.dataframe(df_q1, use_container_width=True)
        
        st.subheader("2. Customer Segmentation by Risk Characteristics")
        q2 = '''
        WITH SegmentedData AS (
            SELECT 
                customerID,
                Contract,
                PaymentMethod,
                TenureGroup,
                Churn,
                CASE 
                    WHEN Contract = 'Month-to-month' AND PaymentMethod = 'Electronic check' THEN 'High Risk (M2M & Elec Check)'
                    WHEN Contract = 'Two year' THEN 'Low Risk (2 Year)'
                    ELSE 'Medium Risk (Other)'
                END AS RiskSegment
            FROM customers
        )
        SELECT 
            RiskSegment,
            COUNT(customerID) AS TotalCustomers,
            SUM(CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END) AS ChurnedCustomers,
            ROUND(SUM(CASE WHEN Churn = 'Yes' THEN 1.0 ELSE 0.0 END) / COUNT(customerID) * 100, 2) AS ChurnRatePercentage
        FROM SegmentedData
        GROUP BY RiskSegment
        ORDER BY ChurnRatePercentage DESC;
        '''
        st.code(q2, language='sql')
        df_q2 = pd.read_sql_query(q2, conn)
        st.dataframe(df_q2, use_container_width=True)
        
        conn.close()

def ml_model_performance():
    st.title("⚙️ Machine Learning Pipeline & Evaluation")
    st.markdown("We trained multiple models using `scikit-learn` to predict churn. Because churn datasets are typically imbalanced, we rely on **ROC-AUC** and **Recall** instead of basic accuracy.")
    
    st.subheader("Model Comparison (Actual Test Set Results)")
    
    # These metrics were derived from the actual train_model.py output
    metrics_data = {
        "Model": ["Logistic Regression", "Random Forest (Selected)", "XGBoost"],
        "Accuracy": ["73.81%", "74.80%", "75.73%"],
        "Precision": ["50.43%", "51.62%", "53.28%"],
        "Recall": ["78.34%", "80.75%", "69.52%"],
        "F1-Score": ["61.36%", "62.98%", "60.32%"],
        "ROC-AUC": ["0.8417", "0.8440", "0.8194"]
    }
    st.dataframe(pd.DataFrame(metrics_data), use_container_width=True)
    
    st.info("**Why Random Forest?**\\n\\nWe selected Random Forest because it achieved the highest ROC-AUC and caught over 80% of true churners (Highest Recall). In churn prediction, missing a churning customer (False Negative) is much more expensive than occasionally targeting a loyal customer (False Positive).")
    
    st.subheader("Confusion Matrix (Random Forest)")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **Predicted: No Churn**
        - True Negative: **752** (Loyal customers correctly identified)
        - False Negative: **72** (Churners missed by the model)
        """)
    with col2:
        st.markdown("""
        **Predicted: Churn**
        - False Positive: **283** (Loyal customers mistakenly flagged)
        - True Positive: **302** (Churners successfully caught)
        """)

def customer_churn_predictor():
    st.title("📉 Customer Churn Risk Predictor")
    st.markdown("Use our trained Random Forest model to predict the probability of a customer churning.")
    
    # Input form
    with st.form("customer_data_form"):
        st.subheader("👤 Customer Profile")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            gender = st.selectbox("Gender", ["Male", "Female"])
            senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
            partner = st.selectbox("Partner", ["Yes", "No"])
            dependents = st.selectbox("Dependents", ["No", "Yes"])
            
        with col2:
            tenure = st.number_input("Tenure (Months)", min_value=0, max_value=100, value=12)
            phone_service = st.selectbox("Phone Service", ["Yes", "No"])
            multiple_lines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
            internet_service = st.selectbox("Internet Service", ["Fiber optic", "DSL", "No"])
            
        with col3:
            contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
            payment_method = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
            monthly_charges = st.number_input("Monthly Charges ($)", min_value=10.0, max_value=150.0, value=70.0)
            total_charges = st.number_input("Total Charges ($)", min_value=0.0, max_value=10000.0, value=tenure * 70.0)
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("🛠️ Additional Services")
        scol1, scol2, scol3, scol4 = st.columns(4)
        with scol1:
            online_security = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
            device_protection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])
        with scol2:
            online_backup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])
            streaming_movies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])
        with scol3:
            tech_support = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
            paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
        with scol4:
            streaming_tv = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
            
        submit_button = st.form_submit_button("Predict Churn Risk")

    if submit_button:
        # Create dataframe for prediction
        input_data = pd.DataFrame({
            'gender': [gender],
            'SeniorCitizen': [senior_citizen],
            'Partner': [partner],
            'Dependents': [dependents],
            'tenure': [tenure],
            'PhoneService': [phone_service],
            'MultipleLines': [multiple_lines],
            'InternetService': [internet_service],
            'OnlineSecurity': [online_security],
            'OnlineBackup': [online_backup],
            'DeviceProtection': [device_protection],
            'TechSupport': [tech_support],
            'StreamingTV': [streaming_tv],
            'StreamingMovies': [streaming_movies],
            'Contract': [contract],
            'PaperlessBilling': [paperless_billing],
            'PaymentMethod': [payment_method],
            'MonthlyCharges': [monthly_charges],
            'TotalCharges': [total_charges]
        })
        
        prob = model.predict_proba(input_data)[0][1]
        
        st.markdown("<hr style='margin: 2rem 0; border-color: #e2e8f0;'>", unsafe_allow_html=True)
        st.subheader("🎯 Prediction Results")
        
        prob_percentage = prob * 100
        
        if prob >= 0.70:
            risk_category = "High Risk 🔴"
            action = "Immediate retention action required. Offer a discount to switch to a 1-year contract."
            border_color = "#ef4444"
        elif prob >= 0.40:
            risk_category = "Medium Risk 🟡"
            action = "Monitor customer. Suggest setting up automatic payments."
            border_color = "#eab308"
        else:
            risk_category = "Low Risk 🟢"
            action = "Customer is stable. No action required."
            border_color = "#22c55e"
            
        colA, colB = st.columns([1, 2])
        with colA:
            st.metric(label="Churn Probability", value=f"{prob_percentage:.1f}%")
        with colB:
            st.markdown(f"""
            <div class="prediction-card" style="border-left-color: {border_color};">
                <h4 style="margin-top: 0; color: #0f172a;">Risk Category: {risk_category}</h4>
                <p style="color: #475569; margin-bottom: 0;"><strong>Recommended Action:</strong> {action}</p>
            </div>
            """, unsafe_allow_html=True)

def retention_strategy():
    st.title("🎯 Retention Strategy & Action Plan")
    st.markdown("Based on the data and predictive model, here is the strategic action plan to reduce churn and maximize MRR (Monthly Recurring Revenue).")
    
    st.subheader("1. High-Risk Customer Prioritization")
    st.info("**Action:** The Retention Team should use the 'Customer Churn Predictor' tool or export the `customer_risk_scores.csv` file. Sort customers by **Risk Category = High** AND **Monthly Charges (Descending)**. This ensures we prioritize saving our highest-paying customers who are most likely to leave.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("2. The 'Bridge-to-Annual' Campaign")
        st.markdown("""
        **Target:** Customers on Month-to-Month contracts nearing their 6th month.
        **Why:** Month-to-month users churn at 42.7%.
        **Tactic:** Offer a free premium add-on (e.g., Tech Support or Online Security) if they commit to a 1-year contract. Do not force them, incentivize them.
        """)
        
    with col2:
        st.subheader("3. The Autopay Incentive")
        st.markdown("""
        **Target:** Customers paying via Electronic Check.
        **Why:** Manual payment creates a monthly decision point to cancel.
        **Tactic:** Offer a $5/month discount or a one-time bill credit for enrolling in automatic Credit Card or Bank Transfer payments.
        """)
        
    st.subheader("4. Measuring Success (A/B Testing)")
    st.markdown("""
    Never roll out a retention discount to everyone at once. We must prove the model's ROI:
    1. Select the top 1,000 High-Risk customers.
    2. **Treatment Group (500):** Receive the proactive retention call/discount.
    3. **Control Group (500):** Business as usual (no intervention).
    4. **Evaluate:** After 30 days, calculate the difference in churn rate between the two groups to determine the exact revenue saved.
    """)

# Define Pages
home_p = st.Page(home_page, title="Home", icon="🏠", default=True)
overview_page = st.Page(executive_overview, title="Executive Overview", icon="📈")
analytics_page = st.Page(customer_analytics, title="Customer Analytics", icon="📊")
sql_page = st.Page(sql_analytics, title="SQL Analytics", icon="💻")
ml_page = st.Page(ml_model_performance, title="ML Model Performance", icon="⚙️")
predictor_page = st.Page(customer_churn_predictor, title="Churn Predictor", icon="🎯")
strategy_page = st.Page(retention_strategy, title="Retention Strategy", icon="💡")

# Main Navigation
pages = {
    "Home": [home_p],
    "Dashboards": [overview_page, analytics_page, sql_page],
    "Machine Learning": [ml_page, predictor_page],
    "Strategy": [strategy_page]
}

pg = st.navigation(pages)
pg.run()
