# etl/clean.py

import pandas as pd
from pathlib import Path

def run_cleaning():
    """
    Cleans the raw retail data and saves it to the curated layer as a Parquet file.
    """
    # Define file paths
    project_root = Path(__file__).resolve().parents[1]
    raw_data_path = project_root / 'data' / 'raw' / 'OnlineRetail.csv'
    curated_data_path = project_root / 'data' / 'curated' / 'cleaned_online_retail.parquet'

    print("--- Starting Data Cleaning Process ---")
    
    # --- 1. Load Data ---
    print(f"Loading raw data from {raw_data_path}...")
    df = pd.read_csv(raw_data_path, encoding='latin1')
    print("Raw data loaded successfully. Initial shape: {df.shape}")

    # --- 2. Handle Missing Values ---
    # For a Customer 360, rows without a CustomerID are not useful.
    df.dropna(subset=['CustomerID'], inplace=True)
    print(f"Shape after dropping rows with missing CustomerID: {df.shape}")

    # --- 3. Correct Data Types ---
    df['CustomerID'] = df['CustomerID'].astype(int).astype(str)
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    print("Corrected data types for CustomerID and InvoiceDate.")

    # --- 4. Remove Cancellations & Invalid Data ---
    # InvoiceNo starting with 'C' are cancellations.
    # We also only want transactions with a positive quantity.
    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]
    df = df[df['Quantity'] > 0]
    print(f"Shape after removing cancellations and zero/negative quantities: {df.shape}")
    
    # --- 5. Remove Duplicates ---
    df.drop_duplicates(inplace=True)
    print(f"Shape after dropping duplicate rows: {df.shape}")

    # --- 6. Standardize Column Names ---
    # Convert to snake_case for consistency (e.g., 'InvoiceNo' -> 'invoice_no')
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    print(f"Standardized column names to snake_case.")

    # --- 7. Save Curated Data ---
    print(f"Saving cleaned data to {curated_data_path}...")
    df.to_parquet(curated_data_path)
    print("--- Data Cleaning Process Finished Successfully! ---")


if __name__ == '__main__':
    run_cleaning()