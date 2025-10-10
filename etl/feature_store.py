# etl/feature_store.py

import pandas as pd
from pathlib import Path

def create_features():
    """
    Creates a customer feature set from the clean data.
    This includes RFM features and a churn label.
    """
    # --- Load Data ---
    project_root = Path(__file__).resolve().parents[1]
    curated_data_path = project_root / 'data' / 'curated' / 'cleaned_online_retail.parquet'
    features_path = project_root / 'data' / 'curated' / 'customer_features.parquet'
    
    print("--- Starting Feature Engineering ---")
    df = pd.read_parquet(curated_data_path)
    df['revenue'] = df['quantity'] * df['unitprice']

    # --- Feature Calculation ---
    # Define a snapshot date. We will calculate features as of this date.
    # Let's take it as one day after the last transaction to include all data.
    snapshot_date = df['invoicedate'].max() + pd.DateOffset(days=1)
    print(f"Snapshot date for feature calculation: {snapshot_date}")

    # Aggregate data to the customer level
    customer_features = df.groupby('customerid').agg({
        'invoicedate': lambda date: (snapshot_date - date.max()).days, # Recency
        'invoiceno': 'nunique',                                    # Frequency
        'revenue': 'sum'                                           # Monetary
    }).rename(columns={
        'invoicedate': 'recency',
        'invoiceno': 'frequency',
        'revenue': 'monetary'
    })

    # --- Churn Label Definition ---
    # We define churn as no purchase in the last 90 days.
    # If a customer's last purchase was more than 90 days ago, they are churned.
    customer_features['churn'] = (customer_features['recency'] > 90).astype(int)
    
    print(f"Feature set created. Shape: {customer_features.shape}")
    print("\nFeature set sample:")
    print(customer_features.head())
    print(f"\nChurn distribution:\n{customer_features['churn'].value_counts(normalize=True)}")

    # --- Save Features ---
    customer_features.to_parquet(features_path)
    print(f"Customer features saved to {features_path}")
    print("--- Feature Engineering Finished ---")

if __name__ == '__main__':
    create_features()