#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get specific HVL lead session data
"""
import os
from google.cloud import bigquery
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set credentials path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(SCRIPT_DIR, "database_access", "affable-album-354309-72260dd4d800.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

PROJECT_ID = "affable-album-354309"
FULL_TABLE_NAME = f"{PROJECT_ID}.e2e_dev.e2e_brokers_log"

def get_hvl_session(session_id):
    """Get specific session with HVL lead information"""
    try:
        logger.info(f"Querying session {session_id}...")
        client = bigquery.Client(project=PROJECT_ID)
        
        query = f"""
        WITH e2e_conversions_users AS (
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
            ON s.user_id = u.id
          LEFT JOIN `{PROJECT_ID}.prod_db.brokers` b
            ON b.slug = eb.broker_slug
        ),
        hvl_sessions AS (
          SELECT 
            session_id,
            MAX(CASE WHEN answer_id IN (157, 158) THEN 1 ELSE 0 END) as hvl_lead
          FROM (
            SELECT 
              session_id,
              question_id,
              answer_id,
              ROW_NUMBER() OVER (
                PARTITION BY session_id, question_id 
                ORDER BY time DESC
              ) as rn
            FROM `{PROJECT_ID}.prod_db.fmb_answers_sessions`
            WHERE question_type = 1
          )
          WHERE rn = 1
          GROUP BY session_id
        )
        SELECT 
          e2e.*,
          COALESCE(hvl.hvl_lead, 0) as hvl_lead
        FROM e2e_conversions_users e2e
        LEFT JOIN hvl_sessions hvl
          ON e2e.session_id = hvl.session_id
        WHERE e2e.session_id = {session_id}
        ORDER BY event_timestamp
        """
        
        result = client.query(query).result()
        df = result.to_dataframe()
        
        logger.info(f"\nSession {session_id} data:")
        logger.info(f"  Events: {len(df)}")
        logger.info(f"  HVL lead: {df['hvl_lead'].iloc[0] if len(df) > 0 else 'N/A'}")
        logger.info(f"\nColumns: {list(df.columns)}")
        logger.info(f"\nData:")
        print(df.to_string())
        
        return df
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise


if __name__ == '__main__':
    print("="*60)
    print("GETTING HVL SESSION DATA")
    print("="*60)
    df = get_hvl_session(231751332)
    print("\n" + "="*60)
