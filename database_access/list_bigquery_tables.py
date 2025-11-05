#!/usr/bin/env python3
"""
Script to list BigQuery datasets and tables
"""

import os
from google.cloud import bigquery

# Set credentials path
CREDENTIALS_PATH = "/home/ubuntu/_dev/_dominik/bc/hackaton/database_access/affable-album-354309-72260dd4d800.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

PROJECT_ID = "affable-album-354309"

def list_datasets_and_tables():
    """List all datasets and their tables"""
    print(f"Connecting to BigQuery project: {PROJECT_ID}")
    
    try:
        # Initialize BigQuery client
        client = bigquery.Client(project=PROJECT_ID)
        
        # List datasets
        print("\n" + "="*60)
        print("AVAILABLE DATASETS:")
        print("="*60)
        
        datasets = list(client.list_datasets())
        
        if not datasets:
            print("No datasets found in this project.")
            return
        
        for dataset in datasets:
            print(f"\nDataset: {dataset.dataset_id}")
            
            # List tables in this dataset
            dataset_ref = client.dataset(dataset.dataset_id)
            tables = list(client.list_tables(dataset_ref))
            
            if tables:
                print(f"  Tables ({len(tables)}):")
                for table in tables:
                    table_ref = client.get_table(table.reference)
                    print(f"    - {table.table_id}")
                    print(f"      Full name: {PROJECT_ID}.{dataset.dataset_id}.{table.table_id}")
                    print(f"      Rows: {table_ref.num_rows:,}")
                    print(f"      Size: {table_ref.num_bytes / (1024*1024):.2f} MB")
            else:
                print("  No tables found in this dataset.")
        
        print("\n" + "="*60)
        
    except Exception as e:
        print(f"\nERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    list_datasets_and_tables()
