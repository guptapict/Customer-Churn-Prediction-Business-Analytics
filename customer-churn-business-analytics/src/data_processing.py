import pandas as pd
import numpy as np
import sqlite3
import os

def clean_data(input_path, output_csv_path, output_db_path):
    print("Loading raw data...")
    df = pd.read_csv(input_path)
    
    print(f"Original shape: {df.shape}")
    
    # 1. TotalCharges is loaded as an object because of blank strings ' '
    # We replace blanks with NaN and convert to numeric
    df['TotalCharges'] = pd.to_numeric(df['TotalCharges'].replace(' ', np.nan))
    
    # Fill missing TotalCharges. Since they correspond to tenure=0, we can fill with 0
    # or drop them (only 11 rows). We will fill with 0 for customers who just joined.
    df['TotalCharges'] = df['TotalCharges'].fillna(0)
    
    # 2. Convert categorical columns
    # 'SeniorCitizen' is 0 or 1, let's map it to 'No' and 'Yes' for consistency in SQL
    df['SeniorCitizen'] = df['SeniorCitizen'].map({0: 'No', 1: 'Yes'})
    
    # 3. Create Tenure Groups (for easier SQL and EDA later)
    # e.g., 0-12 Months, 13-24 Months, etc.
    bins = [-1, 12, 24, 36, 48, 60, 72, 100]
    labels = ['0-12 Months', '13-24 Months', '25-36 Months', '37-48 Months', '49-60 Months', '61-72 Months', '72+ Months']
    df['TenureGroup'] = pd.cut(df['tenure'], bins=bins, labels=labels, right=True)
    
    # 4. Check for duplicates
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        print(f"Dropping {duplicates} duplicate rows.")
        df = df.drop_duplicates()
        
    print(f"Cleaned shape: {df.shape}")
    
    # 5. Save Processed Data to CSV
    print(f"Saving processed data to {output_csv_path}...")
    df.to_csv(output_csv_path, index=False)
    
    # 6. Save Processed Data to SQLite Database
    print(f"Saving data to SQLite database at {output_db_path}...")
    # Create the directory if it doesn't exist (it should, but just in case)
    os.makedirs(os.path.dirname(output_db_path), exist_ok=True)
    
    conn = sqlite3.connect(output_db_path)
    df.to_sql('customers', conn, if_exists='replace', index=False)
    conn.close()
    
    print("Data cleaning and database loading complete.")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RAW_DATA = os.path.join(BASE_DIR, 'data', 'raw', 'Telco-Customer-Churn.csv')
    PROCESSED_DATA = os.path.join(BASE_DIR, 'data', 'processed', 'cleaned_churn_data.csv')
    DB_PATH = os.path.join(BASE_DIR, 'data', 'processed', 'churn_db.sqlite')
    
    clean_data(RAW_DATA, PROCESSED_DATA, DB_PATH)
