import pandas as pd
import numpy as np
import os
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, accuracy_score, precision_score, recall_score, f1_score

def build_model_pipeline(numerical_cols, categorical_cols, model):
    # Preprocessing for numerical data
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])

    # Preprocessing for categorical data
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore', drop='first'))
    ])

    # Bundle preprocessing
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols)
        ])

    # Append classifier to preprocessing pipeline
    clf = Pipeline(steps=[('preprocessor', preprocessor),
                          ('classifier', model)])
    return clf

def evaluate_model(name, model, X_test, y_test):
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    
    acc = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred)
    rec = recall_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred)
    roc_auc = roc_auc_score(y_test, y_prob)
    
    print(f"--- {name} ---")
    print(f"Accuracy:  {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall:    {rec:.4f}")
    print(f"F1 Score:  {f1:.4f}")
    print(f"ROC-AUC:   {roc_auc:.4f}")
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    print("\n")
    
    return {'name': name, 'model': model, 'f1': f1, 'recall': rec, 'roc_auc': roc_auc}

def main():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'cleaned_churn_data.csv')
    
    print("Loading data...")
    df = pd.read_csv(DATA_PATH)
    
    # 1. Prepare Data
    # Drop CustomerID as it has no predictive value
    # Drop TenureGroup as it's perfectly correlated with tenure (we use tenure for the model)
    drop_cols = ['customerID', 'TenureGroup']
    X = df.drop(columns=drop_cols + ['Churn'])
    
    # Target variable (convert to binary)
    y = df['Churn'].map({'Yes': 1, 'No': 0})
    
    # Identify numerical and categorical columns
    numerical_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = X.select_dtypes(include=['object']).columns.tolist()
    
    print(f"Numerical features: {numerical_cols}")
    print(f"Categorical features: {categorical_cols}")
    
    # Stratified Train/Test Split to handle imbalance
    X_train, X_test, y_train, y_test, id_train, id_test = train_test_split(
        X, y, df['customerID'], test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training data shape: {X_train.shape}")
    print(f"Testing data shape: {X_test.shape}")
    
    # 2. Build Models
    models = [
        ('Logistic Regression', LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000)),
        ('Random Forest', RandomForestClassifier(class_weight='balanced', random_state=42, n_estimators=100, max_depth=6)),
        ('XGBoost', XGBClassifier(scale_pos_weight=(len(y_train) - sum(y_train)) / sum(y_train), random_state=42, eval_metric='logloss'))
    ]
    
    results = []
    
    print("Training and evaluating models...\n")
    for name, model in models:
        clf = build_model_pipeline(numerical_cols, categorical_cols, model)
        clf.fit(X_train, y_train)
        res = evaluate_model(name, clf, X_test, y_test)
        results.append(res)
        
    # 3. Select Best Model (Optimizing for Recall/ROC-AUC because False Negatives are costly for Churn)
    # We will pick Logistic Regression or XGBoost based on ROC-AUC
    best_model_info = max(results, key=lambda x: x['roc_auc'])
    print(f"Selected Best Model: {best_model_info['name']} with ROC-AUC = {best_model_info['roc_auc']:.4f}")
    best_model = best_model_info['model']
    
    # 4. Save the Model
    model_path = os.path.join(BASE_DIR, 'models', 'churn_model.pkl')
    joblib.dump(best_model, model_path)
    print(f"Model saved to {model_path}")
    
    # 5. Customer Risk Scoring
    # Generate predictions for the entire dataset to create risk scores for business use
    df_full = X.copy()
    probabilities = best_model.predict_proba(df_full)[:, 1]
    predictions = best_model.predict(df_full)
    
    risk_df = pd.DataFrame({
        'customerID': df['customerID'],
        'ActualChurn': df['Churn'],
        'ChurnProbability': np.round(probabilities, 4),
        'PredictedChurnClass': ['Yes' if p == 1 else 'No' for p in predictions]
    })
    
    # Create Risk Categories based on Probability Thresholds
    # e.g., > 70% High Risk, 40-70% Medium Risk, < 40% Low Risk
    def categorize_risk(prob):
        if prob >= 0.70:
            return 'High Risk'
        elif prob >= 0.40:
            return 'Medium Risk'
        else:
            return 'Low Risk'
            
    risk_df['RiskCategory'] = risk_df['ChurnProbability'].apply(categorize_risk)
    
    predictions_path = os.path.join(BASE_DIR, 'data', 'predictions', 'customer_risk_scores.csv')
    risk_df.to_csv(predictions_path, index=False)
    print(f"Risk scores saved to {predictions_path}")
    print("\nSample of Risk Scores:")
    print(risk_df.head(10))

if __name__ == "__main__":
    main()
