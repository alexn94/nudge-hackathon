#!/usr/bin/env python3
"""
Script to download 10,000 rows from BigQuery table and load into pandas DataFrame
Uses direct table reading instead of query jobs to avoid permission issues.
"""

import os
from google.cloud import bigquery
import pandas as pd
from datetime import datetime

# Set credentials path
CREDENTIALS_PATH = "/home/ubuntu/_dev/_dominik/bc/hackaton/database_access/affable-album-354309-72260dd4d800.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

# BigQuery configuration
PROJECT_ID = "affable-album-354309"
DATASET_ID = "e2e_dev"
TABLE_ID = "e2e_brokers_log"

# Output files
SQL_OUTPUT_FILE = "/home/ubuntu/_dev/_dominik/bc/hackaton/database_access/bigquery_data.sql"
CSV_OUTPUT_FILE = "/home/ubuntu/_dev/_dominik/bc/hackaton/database_access/bigquery_data.csv"

def download_bigquery_data_direct():
    """Download data from BigQuery table directly and save to SQL and CSV files"""
    print(f"Connecting to BigQuery using credentials: {CREDENTIALS_PATH}")
    
    # Initialize BigQuery client
    client = bigquery.Client(project=PROJECT_ID)
    
    # Get table reference
    table_ref = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"
    print(f"\nAccessing table: {table_ref}")
    
    try:
        # Get table object
        table = client.get_table(table_ref)
        
        print(f"\nTable info:")
        print(f"  - Full name: {table.full_table_id}")
        print(f"  - Total rows: {table.num_rows:,}")
        print(f"  - Size: {table.num_bytes / (1024*1024):.2f} MB")
        print(f"  - Schema: {len(table.schema)} columns")
        
        # List rows directly from the table (limit to 10,000)
        print(f"\nDownloading first 10,000 rows...")
        
        rows_iter = client.list_rows(table, max_results=10000)
        
        # Convert to DataFrame
        df = rows_iter.to_dataframe()
        
        print(f"\nSuccessfully downloaded {len(df)} rows with {len(df.columns)} columns")
        print(f"Columns: {list(df.columns)}")
        
        # Save to CSV first (most reliable format)
        print(f"\nSaving data to CSV file: {CSV_OUTPUT_FILE}")
        df.to_csv(CSV_OUTPUT_FILE, index=False)
        print(f"✅ CSV file saved successfully!")
        
        # Save to SQL file (as INSERT statements)
        print(f"\nSaving data to SQL file: {SQL_OUTPUT_FILE}")
        
        with open(SQL_OUTPUT_FILE, 'w', encoding='utf-8') as f:
            # Write header comment
            f.write(f"-- BigQuery data export\n")
            f.write(f"-- Table: {table_ref}\n")
            f.write(f"-- Exported: {datetime.now().isoformat()}\n")
            f.write(f"-- Rows: {len(df)}\n\n")
            
            # Create table definition
            f.write(f"CREATE TABLE IF NOT EXISTS {TABLE_ID} (\n")
            for i, (col_name, col_type) in enumerate(zip(df.columns, df.dtypes)):
                # Map pandas dtypes to SQL types
                if pd.api.types.is_integer_dtype(col_type):
                    sql_type = "BIGINT"
                elif pd.api.types.is_float_dtype(col_type):
                    sql_type = "DOUBLE"
                elif pd.api.types.is_bool_dtype(col_type):
                    sql_type = "BOOLEAN"
                elif pd.api.types.is_datetime64_any_dtype(col_type):
                    sql_type = "TIMESTAMP"
                else:
                    sql_type = "TEXT"
                
                comma = "," if i < len(df.columns) - 1 else ""
                f.write(f"  {col_name} {sql_type}{comma}\n")
            f.write(f");\n\n")
            
            # Write INSERT statements in batches
            batch_size = 100
            for batch_start in range(0, len(df), batch_size):
                batch_end = min(batch_start + batch_size, len(df))
                batch_df = df.iloc[batch_start:batch_end]
                
                f.write(f"INSERT INTO {TABLE_ID} ({', '.join(df.columns)}) VALUES\n")
                
                for row_idx, (idx, row) in enumerate(batch_df.iterrows()):
                    values = []
                    for val in row:
                        if pd.isna(val):
                            values.append("NULL")
                        elif isinstance(val, str):
                            # Escape single quotes and backslashes
                            escaped_val = str(val).replace("\\", "\\\\").replace("'", "''")
                            # Truncate very long strings
                            if len(escaped_val) > 1000:
                                escaped_val = escaped_val[:1000] + "..."
                            values.append(f"'{escaped_val}'")
                        elif isinstance(val, (pd.Timestamp, datetime)):
                            values.append(f"'{val}'")
                        else:
                            values.append(f"'{val}'")
                    
                    value_str = f"  ({', '.join(values)})"
                    
                    # Add comma unless it's the last row in batch
                    if row_idx == len(batch_df) - 1:
                        value_str += ";\n\n"
                    else:
                        value_str += ",\n"
                    
                    f.write(value_str)
        
        print(f"✅ SQL file saved successfully!")
        
        return df
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        raise


def load_from_csv_file():
    """Load data from CSV file into pandas DataFrame"""
    print(f"\n{'='*60}")
    print("LOADING DATA FROM CSV FILE")
    print(f"{'='*60}\n")
    
    print(f"Reading CSV file: {CSV_OUTPUT_FILE}")
    
    try:
        df_loaded = pd.read_csv(CSV_OUTPUT_FILE)
        print(f"✅ Successfully loaded {len(df_loaded)} rows from CSV file")
        return df_loaded
    except Exception as e:
        print(f"❌ ERROR loading CSV: {str(e)}")
        raise


def display_dataframe(df):
    """Display DataFrame information in terminal"""
    print(f"\n{'='*60}")
    print("DATAFRAME INFORMATION")
    print(f"{'='*60}\n")
    
    print(f"Shape: {df.shape} (rows x columns)")
    print(f"\nColumn names and types:")
    print(df.dtypes)
    
    print(f"\n{'='*60}")
    print("FIRST 20 ROWS")
    print(f"{'='*60}\n")
    
    # Set pandas display options for better visibility
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 50)
    
    print(df.head(20))
    
    print(f"\n{'='*60}")
    print("BASIC STATISTICS")
    print(f"{'='*60}\n")
    
    # Only show statistics for numeric columns
    numeric_df = df.select_dtypes(include=['number'])
    if len(numeric_df.columns) > 0:
        print(numeric_df.describe())
    else:
        print("No numeric columns found")
    
    print(f"\n{'='*60}")
    print("NULL VALUE COUNTS")
    print(f"{'='*60}\n")
    
    null_counts = df.isnull().sum()
    null_counts = null_counts[null_counts > 0]  # Only show columns with nulls
    if len(null_counts) > 0:
        print(null_counts)
    else:
        print("No null values found!")


def main():
    """Main function"""
    print("="*60)
    print("BIGQUERY DATA DOWNLOAD AND LOAD SCRIPT")
    print("Direct table reading (no query jobs needed)")
    print("="*60)
    print()
    
    try:
        # Step 1: Download data from BigQuery and save to SQL + CSV files
        print("STEP 1: Downloading from BigQuery...")
        df = download_bigquery_data_direct()
        
        # Step 2: Load from CSV file to demonstrate file loading
        print("\n" + "="*60)
        print("STEP 2: Loading from saved CSV file...")
        df_loaded = load_from_csv_file()
        
        # Step 3: Display in terminal
        print("\n" + "="*60)
        print("STEP 3: Displaying data...")
        display_dataframe(df_loaded)
        
        print("\n" + "="*60)
        print("✅ SCRIPT COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"\nFiles created:")
        print(f"  - SQL file: {SQL_OUTPUT_FILE}")
        print(f"  - CSV file: {CSV_OUTPUT_FILE}")
        
    except Exception as e:
        print(f"\n❌ SCRIPT FAILED!")
        print(f"ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
