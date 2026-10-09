# Model Evaluation Report

## 1. Overview
The goal of this phase was to build a machine learning model capable of predicting customer churn. We prepared the data using a `ColumnTransformer` (StandardScaler for numerical features, OneHotEncoder for categorical features) and avoided data leakage by fitting the transformations only on the training set.

Given the class imbalance (only 26.5% of customers churned), we focused on **Recall** and **ROC-AUC** rather than simple Accuracy. In churn prediction, a False Negative (failing to identify a churning customer) is typically more costly than a False Positive (offering a retention discount to a loyal customer).

## 2. Models Evaluated
We trained three models, handling class imbalance natively via `class_weight` and `scale_pos_weight`:
1. **Logistic Regression**
2. **Random Forest Classifier**
3. **XGBoost Classifier**

### Results on Test Set (20% of data)

| Model | Accuracy | Precision | Recall | F1 Score | ROC-AUC |
|---|---|---|---|---|---|
| **Logistic Regression** | 73.81% | 50.43% | 78.34% | 61.36% | 0.8417 |
| **Random Forest** | **74.80%** | **51.62%** | **80.75%** | **62.98%** | **0.8440** |
| **XGBoost** | 75.73% | 53.28% | 69.52% | 60.32% | 0.8194 |

## 3. Best Model Selection
**Random Forest** was selected as the best model for this business problem.
* It achieved the highest **ROC-AUC (0.8440)**, meaning it is the best at distinguishing between churners and non-churners overall.
* It achieved an excellent **Recall of 80.75%**. This means the model successfully catches over 80% of all customers who will actually churn.
* **Trade-off:** The precision is ~51.6%, meaning about half the customers we flag as "at-risk" won't actually churn. In a business context, offering low-cost retention interventions (like a check-in call or a small discount) to these False Positives is an acceptable trade-off for catching 80% of the true churners.

## 4. Customer Risk Scoring
We generated a probability score (0.0 to 1.0) for every customer and categorized them into Risk Segments based on these thresholds:
* **High Risk:** > 70% Probability
* **Medium Risk:** 40% - 70% Probability
* **Low Risk:** < 40% Probability

These risk scores are exported to `data/predictions/customer_risk_scores.csv` and are ready to be integrated into the Power BI Dashboard to guide the retention team.
