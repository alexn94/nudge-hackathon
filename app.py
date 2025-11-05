# -*- coding: utf-8 -*-
"""
BrokerChooser Flask app with Nuclia AI chatbot integration
"""
from flask import Flask, render_template, request, Response, send_from_directory
import requests
import logging
import json
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Nuclia configuration
NUCLIA_API_KEY = "eyJhbGciOiJSUzI1NiIsImtpZCI6InNhIiwidHlwIjoiSldUIn0.eyJpc3MiOiJodHRwczovL2V1cm9wZS0xLm51Y2xpYS5jbG91ZC8iLCJpYXQiOjE3NjIxODM1NTAsInN1YiI6IjQ1MTE0ZTFmLTZkZmEtNDkwZC1iN2ZkLWVkYmJjMmZhNTc5YSIsImp0aSI6IjJjMGIxOGNmLWM1ZjgtNGZjNi04ODVjLTdlZDNhZDQwZGZiNCIsImV4cCI6MTc5MzcxOTU0OSwia2V5IjoiYWY2ODYwMDAtMzQ4Zi00NWUwLTgzMGItOTI5MThlNTAxZjUyIiwia2lkIjoiMjg4NzdlOTgtZWZlMC00YjM2LWIyYjctN2I4YWQ2MTdmZTE4In0.geM880M25Nj_z-ds3uvd2CxyPbEBAU0xq-sy_oscoWGDlCNLYbndA9FgLthuugN_I6HyQOUIzUvZwE_crnKNireA8tRgki-2Y27AMa7-N0VRS1HLKJaYvJCmLOqlY-2hT3xWdsLI2ZIR05fbY3cc1oosr4wK5UDGluTf9vt88sqCsrrySvsrJ07PTaDA5eKpNq0F9jwvIjNOj4lj9dyu0jOAIz2mPSoPu_OCuDwYdBnywKdmsTP_CoBeDFNqHFR_A6HBUkyQzXWa9vMnGAUzS9rHVlE6VzM0fPa4LeizPoPrnhKCwur6alKEl22PheDl7OH_SVz-602u232Xjvde1DAaiePaddIZhDlI6bKITC44aHB-_RvvFQ4_xWseONRAuHhnbdvbdLCOIW7GuAxo1rbx2v3MnqPpkcK8E7hRzcKwjTvjdnzDa8MTOHN_cgUuo-PrCpx9CabCSUGM_AXULTwR1oQzq5tnBD31fzpuymGk8Ya4fuKJolgzgCrHU2bhizXobRjbJoQRCaT8qcG67g11i94hw7qCNeI-asbsrMfq4RUyuqNtSIlmIiglApaqpZWs2nuGpy89U3OGyJNJWswjDACKX6dYEDwcW6kzibZ_uZE30KuzVO5388L4NYHR9ysuTYuiTJoUFKBpFkCWDABm6i2lgnEkAt5hjYQSZM8"
NUCLIA_KB_ID = "17d17844-3acb-4c8f-92bf-1b7aec85b05c"
NUCLIA_API_ENDPOINT = f"https://europe-1.rag.progress.cloud/api/v1/kb/{NUCLIA_KB_ID}/ask"


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
                    'message': answer,
                    'citations': citations[:5]  # Limit to top 5 citations
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
    Initialize chat with a predefined question to Nuclia
    This is called automatically when the page loads
    """
    try:
        # Predefined initialization message
        init_message = "Greet me in English and remind me that I forgot to complete my registration on the Interactive Brokers (IBKR) platform. Ask if you can help me finish the process or if I have any questions."
        
        logger.info("Initializing chat with predefined message")
        
        headers = {
            'Content-Type': 'application/json',
            'X-NUCLIA-SERVICEACCOUNT': f'Bearer {NUCLIA_API_KEY}'
        }
        
        payload = {
            'query': init_message,
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
            try:
                response_text = response.text
                
                # Parse NDJSON (streaming format) - collect all text chunks
                lines = response_text.strip().split('\n')
                answer_parts = []
                
                for line in lines:
                    if line.strip():
                        try:
                            line_data = json.loads(line)
                            # Nuclia streaming format: {"item":{"type":"answer","text":"..."}}
                            if 'item' in line_data and line_data['item'].get('type') == 'answer':
                                text_chunk = line_data['item'].get('text', '')
                                answer_parts.append(text_chunk)
                        except json.JSONDecodeError:
                            continue
                
                answer = ''.join(answer_parts) if answer_parts else 'Hi! Can I help you with anything related to Interactive Brokers?'
                        
            except Exception as parse_error:
                logger.error(f"Error parsing response: {parse_error}")
                answer = 'Hi! Can I help you with anything related to Interactive Brokers?'
            
            logger.info(f"Init response: {answer[:100] if len(answer) > 100 else answer}")
            
            return Response(
                json.dumps({'success': True, 'message': answer}, ensure_ascii=False),
                mimetype='application/json; charset=utf-8'
            )
        else:
            logger.error(f"Nuclia API error during init: {response.status_code}")
            return Response(
                json.dumps({'success': True, 'message': 'Hi! Can I help you with anything related to Interactive Brokers?'}, ensure_ascii=False),
                mimetype='application/json; charset=utf-8'
            )
            
    except Exception as e:
        logger.error(f"Error in init-chat endpoint: {str(e)}")
        # Return a fallback message instead of error
        return Response(
            json.dumps({'success': True, 'message': 'Szia! Segíthetek valamiben az Interactive Brokers-szel kapcsolatban?'}, ensure_ascii=False),
            mimetype='application/json; charset=utf-8'
        )


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
