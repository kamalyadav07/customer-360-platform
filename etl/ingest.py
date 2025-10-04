# etl/ingest.py

import pandas as pd
from pathlib import Path

def run_ingestion():
    """
    Ingests the raw data from the source CSV file and prints basic info.
    """
    project_root = Path(__file__).resolve().parents[1]
    # Corrected filename to match your CSV file
    raw_data_path = project_root / 'data' / 'raw' / 'OnlineRetail.csv'

    print(f"Loading data from: {raw_data_path}")

    if not raw_data_path.exists():
        print(f"Error: Data file not found at {raw_data_path}")
        return

    try:
        # CORRECTED: Use pd.read_csv() for .csv files
        # Added encoding='latin1' which is needed for this specific dataset
        df = pd.read_csv(raw_data_path, encoding='latin1')
        
        print("Data loaded successfully!")
        
        print("\nFirst 5 rows of the dataset:")
        print(df.head())

        print(f"\nDataset dimensions (rows, columns): {df.shape}")
        
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")


if __name__ == '__main__':
    run_ingestion()