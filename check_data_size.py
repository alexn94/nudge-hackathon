#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check how much data we have in BigQuery
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
FULL_TABLE_NAME = f"{PROJECT_ID}.e2e_dev.e2e_brokers_log"

def check_data_size():
    """Check total data size"""
    try:
        logger.info("Connecting to BigQuery...")
        client = bigquery.Client(project=PROJECT_ID)
        
        # Count total rows in the full query
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
          COUNT(*) as total_rows,
          COUNT(DISTINCT e2e.session_id) as unique_sessions,
          SUM(CASE WHEN COALESCE(hvl.hvl_lead, 0) = 1 THEN 1 ELSE 0 END) as hvl_rows,
          COUNT(DISTINCT CASE WHEN COALESCE(hvl.hvl_lead, 0) = 1 THEN e2e.session_id END) as hvl_sessions
        FROM e2e_conversions_users e2e
        LEFT JOIN hvl_sessions hvl
          ON e2e.session_id = hvl.session_id
        """
        
        logger.info("Counting total rows...")
        result = client.query(query).result()
        
        for row in result:
            total_rows = row.total_rows
            unique_sessions = row.unique_sessions
            hvl_rows = row.hvl_rows
            hvl_sessions = row.hvl_sessions
            
            logger.info(f"\n{'='*60}")
            logger.info(f"ADATMÉRET ÖSSZESÍTÉS")
            logger.info(f"{'='*60}")
            logger.info(f"📊 ÖSSZES ADAT:")
            logger.info(f"   Total rows: {total_rows:,}")
            logger.info(f"   Unique sessions: {unique_sessions:,}")
            logger.info(f"   HVL lead rows: {hvl_rows:,}")
            logger.info(f"   HVL lead sessions: {hvl_sessions:,}")
            logger.info(f"\n📥 LETÖLTÖTT ADAT:")
            logger.info(f"   Downloaded rows: 10,000")
            logger.info(f"   Downloaded percentage: {10000/total_rows*100:.1f}%")
            logger.info(f"\n❌ MIÉRT NEM VOLT BENNE A HVL LEAD:")
            logger.info(f"   A letöltés az event_timestamp szerint rendezve történt")
            logger.info(f"   Az első 10,000 sor a legrégebbi eseményeket tartalmazza")
            logger.info(f"   A HVL lead session (231751332) egy újabb esemény (2025-10-28)")
            logger.info(f"   ezért nem volt benne az első 10,000 sorban")
            logger.info(f"\n💾 TELJES LETÖLTÉS MÉRETE:")
            
            # Estimate file sizes
            avg_row_size = 200  # bytes (becsült)
            total_size_mb = (total_rows * avg_row_size) / (1024 * 1024)
            downloaded_size_mb = (10000 * avg_row_size) / (1024 * 1024)
            
            logger.info(f"   Becsült teljes méret: ~{total_size_mb:.1f} MB")
            logger.info(f"   Becsült letöltött méret: ~{downloaded_size_mb:.1f} MB")
            logger.info(f"{'='*60}\n")
        
    except Exception as e:
        logger.error(f"Error: {e}")
        raise


if __name__ == '__main__':
    check_data_size()
