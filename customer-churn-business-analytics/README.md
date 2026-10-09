# Customer Churn Prediction & Business Analytics

![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Machine_Learning-orange?logo=scikit-learn)
![Power BI](https://img.shields.io/badge/Power_BI-Dashboarding-yellow?logo=powerbi)
![Status](https://img.shields.io/badge/Status-Completed-success)

## 📌 Project Overview
This project is an end-to-end Data Science and Data Analytics solution designed to predict customer churn and extract actionable business insights. By analyzing customer behavior and utilizing machine learning, the project identifies high-risk customers, allowing businesses to optimize retention strategies and reduce revenue loss.

## 💼 Business Problem
Retaining an existing customer is significantly cheaper than acquiring a new one. The primary goals of this project were to:
1. Identify customers who are most likely to churn.
2. Uncover the key factors driving customer churn (e.g., tenure, pricing, contract type).
3. Provide actionable recommendations and an interactive dashboard to improve customer retention.

## 📊 Dataset
- **Source:** [IBM Telco Customer Churn Dataset](https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv)
- **Context:** Contains 7,043 customer records with data on demographics, services, contract types, payment methods, and churn status.

## 🛠️ Tools & Technologies
- **Languages:** Python, SQL (SQLite)
- **Data Processing & EDA:** Pandas, NumPy, Matplotlib, Seaborn
- **Machine Learning:** Scikit-learn (Logistic Regression, Random Forest), XGBoost
- **Business Intelligence:** Power BI (DAX, Interactive Dashboards)

## 🏗️ Architecture & Workflow
1. **Data Ingestion & Cleaning:** Handled missing values (e.g., blank strings in `TotalCharges`), corrected data types, and created new features like `TenureGroup`.
2. **SQL Analytics:** Loaded cleaned data into an SQLite database to perform aggregated queries on churn rates across segments.
3. **Exploratory Data Analysis (EDA):** Visualized the impact of pricing, contracts, and payment methods on churn.
4. **Machine Learning Pipeline:** Built a `ColumnTransformer` (StandardScaler + OneHotEncoder), utilized stratified splitting, and trained classification models handling severe class imbalance.
5. **Dashboarding:** Exported predictive risk scores and historical data into Power BI to create an interactive retention tool.

## 📈 Key Findings (EDA & SQL)
- **Baseline Churn:** The overall churn rate is 26.54%.
- **The Contract Trap:** Month-to-month contracts have a staggering **42.7% churn rate**, compared to just 2.8% for 2-year contracts.
- **Early Attrition:** Customers in their first 12 months are at the highest risk (47.4% churn).
- **Payment Friction:** Customers paying manually via "Electronic check" churn at severely high rates compared to automated methods.

## 🤖 Machine Learning Results
Given the class imbalance, the models were evaluated primarily on **ROC-AUC** and **Recall**, as missing a true churner (False Negative) is highly costly.

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression | 73.81% | 50.43% | 78.34% | 61.36% | 0.8417 |
| **Random Forest (Selected)** | **74.80%** | **51.62%** | **80.75%** | **62.98%** | **0.8440** |
| XGBoost | 75.73% | 53.28% | 69.52% | 60.32% | 0.8194 |

*The Random Forest model was selected because it successfully identified over 80% of all churning customers, allowing the business to proactively intervene.*

## 🚀 Setup & Execution
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run data processing: `python src/data_processing.py`
4. Run ML model training: `python src/train_model.py`
5. Open Power BI Desktop, import the CSVs from `data/processed/` and `data/predictions/`, and follow the `powerbi/dashboard_guide.md`.

## ⚠️ Limitations & Future Improvements
- **Correlation vs. Causation:** The model identifies predictive associations, not causal effects. Forcing a user onto a 1-year contract might not reduce their churn risk if the underlying product dissatisfaction remains.
- **Financial Impact Estimates:** Currently, we assume all false positives cost the same. Future iterations should incorporate a cost-benefit matrix to optimize the classification threshold based on the exact cost of a retention campaign.
