# -*- coding: utf-8 -*-
"""
BigQuery Session Loader
Directly queries BigQuery for specific session data without downloading entire dataset
"""
import os
from google.cloud import bigquery
import pandas as pd
import logging

logger = logging.getLogger(__name__)

# Set credentials path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(SCRIPT_DIR, "database_access", "affable-album-354309-72260dd4d800.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

# BigQuery configuration
PROJECT_ID = "affable-album-354309"
DATASET_ID = "e2e_dev"
TABLE_ID = "e2e_brokers_log"
FULL_TABLE_NAME = f"{PROJECT_ID}.{DATASET_ID}.{TABLE_ID}"


def get_session_data(session_id):
    """
    Query BigQuery directly for a specific session_id
    
    Args:
        session_id: The session ID to query for
        
    Returns:
        pandas.DataFrame: User events for this session
    """
    try:
        logger.info(f"Querying BigQuery for session_id: {session_id}")
        
        # Initialize BigQuery client
        client = bigquery.Client(project=PROJECT_ID)
        
        # SQL query to get session data with user information and broker name
        query = f"""
        WITH e2e_conversions_users as (
          SELECT 
              eb.*,
              ec.session_id,
              u.id as user_id,
              u.name,
              u.email,
              b.name as broker_name
          FROM `{FULL_TABLE_NAME}` eb
          LEFT JOIN `{PROJECT_ID}.prod_db.e2e_conversions` ec
              ON eb.e2e_conversions_id = ec.id
          LEFT JOIN `{PROJECT_ID}.prod_db.sessions` s
            ON ec.session_id = s.id
          LEFT JOIN `{PROJECT_ID}.prod_db.users` u
            ON s.user_id=u.id
          LEFT JOIN `{PROJECT_ID}.prod_db.brokers` b
            ON b.slug=eb.broker_slug
        )
        SELECT 
          *
        FROM
          e2e_conversions_users
        WHERE session_id = {session_id}
        ORDER BY event_timestamp
        """
        
        # Execute query
        query_job = client.query(query)
        results = query_job.result()
        
        # Convert to DataFrame
        df = results.to_dataframe()
        
        logger.info(f"Found {len(df)} events for session_id {session_id}")
        return df
        
    except Exception as e:
        logger.error(f"Error querying BigQuery for session {session_id}: {e}")
        return pd.DataFrame()  # Return empty DataFrame on error


if __name__ == '__main__':
    # Test
    test_session_id = 76109074.0
    print(f"Testing BigQuery session loader with session_id: {test_session_id}")
    df = get_session_data(test_session_id)
    print(f"\nFound {len(df)} events")
    if len(df) > 0:
        print(f"\nColumns: {list(df.columns)}")
        print(f"\nData:\n{df}")
