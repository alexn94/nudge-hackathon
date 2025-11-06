#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check for HVL leads in BigQuery
"""
import os
from google.cloud import bigquery
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set credentials path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_PATH = os.path.join(SCRIPT_DIR, "database_access", "affable-album-354309-72260dd4d800.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = CREDENTIALS_PATH

PROJECT_ID = "affable-album-354309"

def check_hvl_leads():
    """Check for HVL leads in BigQuery"""
    try:
        logger.info("Connecting to BigQuery...")
        client = bigquery.Client(project=PROJECT_ID)
        
        # First, check if there are any answer_id 157 or 158
        query1 = f"""
        SELECT 
            COUNT(*) as total_answers,
            COUNT(DISTINCT session_id) as unique_sessions
        FROM `{PROJECT_ID}.prod_db.fmb_answers_sessions`
        WHERE question_type = 1
          AND answer_id IN (157, 158)
        """
        
        logger.info("Checking for answer_id 157 or 158...")
        result1 = client.query(query1).result()
        for row in result1:
            logger.info(f"  Total answers with 157/158: {row.total_answers}")
            logger.info(f"  Unique sessions: {row.unique_sessions}")
        
        # Get some example sessions with HVL lead
        query2 = f"""
        WITH hvl_sessions AS (
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
          session_id,
          hvl_lead
        FROM hvl_sessions
        WHERE hvl_lead = 1
        LIMIT 10
        """
        
        logger.info("\nGetting example HVL lead sessions...")
        result2 = client.query(query2).result()
        hvl_sessions = list(result2)
        
        if hvl_sessions:
            logger.info(f"Found {len(hvl_sessions)} HVL lead sessions:")
            for row in hvl_sessions:
                logger.info(f"  session_id: {row.session_id}")
        else:
            logger.info("  No HVL lead sessions found")
        
        # Now check if any of these sessions have e2e conversions
        if hvl_sessions:
            session_ids = [str(int(row.session_id)) for row in hvl_sessions]
            session_ids_str = ', '.join(session_ids)
            
            query3 = f"""
            WITH e2e_conversions_users AS (
              SELECT 
                  eb.*,
                  ec.session_id,
                  u.id as user_id,
                  u.name,
                  u.email,
                  b.name as broker_name
              FROM `{PROJECT_ID}.e2e_dev.e2e_brokers_log` eb
              LEFT JOIN `{PROJECT_ID}.prod_db.e2e_conversions` ec
                  ON eb.e2e_conversions_id = ec.id
              LEFT JOIN `{PROJECT_ID}.prod_db.sessions` s
                ON ec.session_id = s.id
              LEFT JOIN `{PROJECT_ID}.prod_db.users` u
                ON s.user_id = u.id
              LEFT JOIN `{PROJECT_ID}.prod_db.brokers` b
                ON b.slug = eb.broker_slug
            )
            SELECT 
              session_id,
              COUNT(*) as event_count
            FROM e2e_conversions_users
            WHERE session_id IN ({session_ids_str})
            GROUP BY session_id
            """
            
            logger.info("\nChecking if HVL sessions have e2e conversions...")
            result3 = client.query(query3).result()
            e2e_sessions = list(result3)
            
            if e2e_sessions:
                logger.info(f"Found {len(e2e_sessions)} HVL sessions with e2e conversions:")
                for row in e2e_sessions:
                    logger.info(f"  session_id: {row.session_id}, events: {row.event_count}")
            else:
                logger.info("  No HVL sessions with e2e conversions found")
                logger.info("  This means HVL leads don't have conversion events in e2e_brokers_log")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise


if __name__ == '__main__':
    print("="*60)
    print("CHECKING FOR HVL LEADS")
    print("="*60)
    check_hvl_leads()
    print("\n" + "="*60)
