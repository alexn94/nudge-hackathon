# -*- coding: utf-8 -*-
"""
BrokerChooser Flask app with Nuclia AI chatbot integration
"""
from flask import Flask, render_template, request, Response, send_from_directory
import requests
import logging
import json
import os
import subprocess
from user_journey_analyzer import UserJourneyAnalyzer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Nuclia configuration
NUCLIA_API_KEY = "eyJhbGciOiJSUzI1NiIsImtpZCI6InNhIiwidHlwIjoiSldUIn0.eyJpc3MiOiJodHRwczovL2V1cm9wZS0xLm51Y2xpYS5jbG91ZC8iLCJpYXQiOjE3NjIxODM1NTAsInN1YiI6IjQ1MTE0ZTFmLTZkZmEtNDkwZC1iN2ZkLWVkYmJjMmZhNTc5YSIsImp0aSI6IjJjMGIxOGNmLWM1ZjgtNGZjNi04ODVjLTdlZDNhZDQwZGZiNCIsImV4cCI6MTc5MzcxOTU0OSwia2V5IjoiYWY2ODYwMDAtMzQ4Zi00NWUwLTgzMGItOTI5MThlNTAxZjUyIiwia2lkIjoiMjg4NzdlOTgtZWZlMC00YjM2LWIyYjctN2I4YWQ2MTdmZTE4In0.geM880M25Nj_z-ds3uvd2CxyPbEBAU0xq-sy_oscoWGDlCNLYbndA9FgLthuugN_I6HyQOUIzUvZwE_crnKNireA8tRgki-2Y27AMa7-N0VRS1HLKJaYvJCmLOqlY-2hT3xWdsLI2ZIR05fbY3cc1oosr4wK5UDGluTf9vt88sqCsrrySvsrJ07PTaDA5eKpNq0F9jwvIjNOj4lj9dyu0jOAIz2mPSoPu_OCuDwYdBnywKdmsTP_CoBeDFNqHFR_A6HBUkyQzXWa9vMnGAUzS9rHVlE6VzM0fPa4LeizPoPrnhKCwur6alKEl22PheDl7OH_SVz-602u232Xjvde1DAaiePaddIZhDlI6bKITC44aHB-_RvvFQ4_xWseONRAuHhnbdvbdLCOIW7GuAxo1rbx2v3MnqPpkcK8E7hRzcKwjTvjdnzDa8MTOHN_cgUuo-PrCpx9CabCSUGM_AXULTwR1oQzq5tnBD31fzpuymGk8Ya4fuKJolgzgCrHU2bhizXobRjbJoQRCaT8qcG67g11i94hw7qCNeI-asbsrMfq4RUyuqNtSIlmIiglApaqpZWs2nuGpy89U3OGyJNJWswjDACKX6dYEDwcW6kzibZ_uZE30KuzVO5388L4NYHR9ysuTYuiTJoUFKBpFkCWDABm6i2lgnEkAt5hjYQSZM8"
NUCLIA_KB_ID = "17d17844-3acb-4c8f-92bf-1b7aec85b05c"
NUCLIA_API_ENDPOINT = f"https://europe-1.rag.progress.cloud/api/v1/kb/{NUCLIA_KB_ID}/ask"

# Initialize User Journey Analyzer
user_analyzer = None


def refresh_bigquery_data():
    """Refresh BigQuery data before starting the app"""
    logger.info("Refreshing BigQuery data...")
    try:
        result = subprocess.run(
            ['python3', 'download_and_load_bigquery.py'],
            cwd='database_access',
            capture_output=True,
            text=True,
            timeout=120
        )
        if result.returncode == 0:
            logger.info("BigQuery data refreshed successfully")
            return True
        else:
            logger.error(f"Error refreshing BigQuery data: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"Exception while refreshing BigQuery data: {e}")
        return False


def initialize_analyzer():
    """Initialize the user journey analyzer"""
    global user_analyzer
    try:
        user_analyzer = UserJourneyAnalyzer()
        user_analyzer.load_data()
        
        # Log analytics summary
        summary = user_analyzer.get_analytics_summary()
        logger.info(f"User Journey Summary: {json.dumps(summary, indent=2, default=str)}")
        
        return True
    except Exception as e:
        logger.error(f"Error initializing analyzer: {e}")
        return False


@app.route('/')
def index():
    """Render the BrokerChooser page with Nuclia"""
    return render_template('brokerchooser.html')


@app.route('/simple')
def simple():
    """Render the simple page"""
    return render_template('index.html')


@app.route('/BrokerChooser_fooldal_files/<path:filename>')
def brokerchooser_assets(filename):
    """Serve BrokerChooser assets"""
    return send_from_directory('BrokerChooser_fooldal_files', filename)


@app.route('/build2/assets/<path:filename>')
def build_assets(filename):
    """Serve build assets"""
    if filename == 'hero-section-image-CEdh6PoK.webp':
        return send_from_directory('static', 'hero-section-image.webp')
    return send_from_directory('BrokerChooser_fooldal_files', filename)


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Proxy endpoint for Nuclia chat API
    Receives user message and forwards it to Nuclia
    """
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return Response(
                json.dumps({'error': 'No message provided'}, ensure_ascii=False),
                status=400,
                mimetype='application/json; charset=utf-8'
            )
        
        logger.info(f"User message: {user_message}")
        
        # Prepare Nuclia API request
        headers = {
            'Content-Type': 'application/json',
            'X-NUCLIA-SERVICEACCOUNT': f'Bearer {NUCLIA_API_KEY}'
        }
        
        payload = {
            'query': user_message,
            'context': []
        }
        
        # Call Nuclia API
        response = requests.post(
            NUCLIA_API_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        # Force UTF-8 encoding
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            # Initialize variables before try block
            citations = []
            try:
                response_text = response.text
                
                # Parse NDJSON (streaming format) - collect all text chunks and citations
                lines = response_text.strip().split('\n')
                answer_parts = []
                
                for line in lines:
                    if line.strip():
                        try:
                            line_data = json.loads(line)
                            item = line_data.get('item', {})
                            item_type = item.get('type', '')
                            
                            # Collect answer text
                            if item_type == 'answer':
                                text_chunk = item.get('text', '')
                                answer_parts.append(text_chunk)
                            
                            # Collect citations from retrieval results
                            elif item_type == 'retrieval':
                                results = item.get('results', {})
                                resources = results.get('resources', {})
                                
                                # Extract citation information from resources
                                for resource_id, resource_data in resources.items():
                                    citation_info = {
                                        'title': resource_data.get('title', 'Untitled'),
                                        'url': '',  # Nuclia doesn't always provide URLs in this format
                                        'paragraphs': []
                                    }
                                    
                                    # Extract paragraphs from fields
                                    fields = resource_data.get('fields', {})
                                    for field_name, field_data in fields.items():
                                        paragraphs_data = field_data.get('paragraphs', {})
                                        for para_id, para_info in paragraphs_data.items():
                                            citation_info['paragraphs'].append({
                                                'text': para_info.get('text', ''),
                                                'score': para_info.get('score', 0)
                                            })
                                    
                                    if citation_info['paragraphs']:  # Only add if has paragraphs
                                        citations.append(citation_info)
                                        
                        except json.JSONDecodeError:
                            continue
                
                answer = ''.join(answer_parts) if answer_parts else 'Sorry, I cannot answer this question.'
                        
            except Exception as parse_error:
                logger.error(f"Error parsing response: {parse_error}")
                answer = 'Sorry, I cannot answer this question.'
            
            logger.info(f"Nuclia response: {answer[:100] if len(answer) > 100 else answer}...")
            logger.info(f"Citations found: {len(citations)}")
            
            return Response(
                json.dumps({
                    'success': True, 
                    'message': answer
                    # Citations removed - they were often irrelevant
                }, ensure_ascii=False),
                mimetype='application/json; charset=utf-8'
            )
        else:
            logger.error(f"Nuclia API error: {response.status_code} - {response.text}")
            return Response(
                json.dumps({'success': False, 'error': 'Failed to get response from Nuclia'}, ensure_ascii=False),
                status=500,
                mimetype='application/json; charset=utf-8'
            )
            
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return Response(
            json.dumps({'success': False, 'error': str(e)}, ensure_ascii=False),
            status=500,
            mimetype='application/json; charset=utf-8'
        )


@app.route('/api/init-chat', methods=['POST'])
def init_chat():
    """
    Initialize chat with instant personalized welcome message and suggested questions
    No Nuclia API call - instant response
    """
    try:
        # Generate instant welcome response based on user journey
        if user_analyzer:
            welcome_response = user_analyzer.generate_welcome_response()
            logger.info(f"Generated welcome message: {welcome_response['message']}")
            logger.info(f"Suggested questions: {welcome_response['suggested_questions']}")
        else:
            # Fallback message if analyzer not initialized
            welcome_response = {
                'message': 'Hi there! 👋 Welcome! Looking for the perfect broker?',
                'suggested_questions': [
                    '🔍 What are the best brokers for beginners?',
                    '💰 Which brokers have the lowest fees?',
                    '🌍 Which brokers are available in my country?'
                ]
            }
            logger.warning("User analyzer not initialized, using fallback message")
        
        # Return instant response with message and suggested questions
        return Response(
            json.dumps({
                'success': True, 
                'message': welcome_response['message'],
                'suggested_questions': welcome_response['suggested_questions']
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8'
        )
            
    except Exception as e:
        logger.error(f"Error in init-chat endpoint: {str(e)}")
        import traceback
        traceback.print_exc()
        # Return a fallback message instead of error
        return Response(
            json.dumps({
                'success': True, 
                'message': 'Hi there! 👋 How can I help you today?',
                'suggested_questions': [
                    '🔍 What are the best brokers?',
                    '💰 Tell me about broker fees',
                    '❓ How do I choose a broker?'
                ]
            }, ensure_ascii=False),
            mimetype='application/json; charset=utf-8'
        )


if __name__ == '__main__':
    logger.info("="*60)
    logger.info("STARTING BROKERCHOOSER APP")
    logger.info("="*60)
    
    # Step 1: BigQuery data refresh disabled - we now query on-demand per session
    logger.info("Step 1: Skipped BigQuery bulk refresh (on-demand queries enabled)")
    
    # Step 2: Initialize user journey analyzer
    logger.info("Step 2: Initializing user journey analyzer...")
    if not initialize_analyzer():
        logger.warning("Failed to initialize analyzer, personalization will be limited")
    
    logger.info("="*60)
    logger.info("APP INITIALIZATION COMPLETE")
    logger.info("="*60)
    
    # Start Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
