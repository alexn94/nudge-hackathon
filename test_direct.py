#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Direct test of the chat function logic
"""
import requests
import json

NUCLIA_API_KEY = "eyJhbGciOiJSUzI1NiIsImtpZCI6InNhIiwidHlwIjoiSldUIn0.eyJpc3MiOiJodHRwczovL2V1cm9wZS0xLm51Y2xpYS5jbG91ZC8iLCJpYXQiOjE3NjIxODM1NTAsInN1YiI6IjQ1MTE0ZTFmLTZkZmEtNDkwZC1iN2ZkLWVkYmJjMmZhNTc5YSIsImp0aSI6IjJjMGIxOGNmLWM1ZjgtNGZjNi04ODVjLTdlZDNhZDQwZGZiNCIsImV4cCI6MTc5MzcxOTU0OSwia2V5IjoiYWY2ODYwMDAtMzQ4Zi00NWUwLTgzMGItOTI5MThlNTAxZjUyIiwia2lkIjoiMjg4NzdlOTgtZWZlMC00YjM2LWIyYjctN2I4YWQ2MTdmZTE4In0.geM880M25Nj_z-ds3uvd2CxyPbEBAU0xq-sy_oscoWGDlCNLYbndA9FgLthuugN_I6HyQOUIzUvZwE_crnKNireA8tRgki-2Y27AMa7-N0VRS1HLKJaYvJCmLOqlY-2hT3xWdsLI2ZIR05fbY3cc1oosr4wK5UDGluTf9vt88sqCsrrySvsrJ07PTaDA5eKpNq0F9jwvIjNOj4lj9dyu0jOAIz2mPSoPu_OCuDwYdBnywKdmsTP_CoBeDFNqHFR_A6HBUkyQzXWa9vMnGAUzS9rHVlE6VzM0fPa4LeizPoPrnhKCwur6alKEl22PheDl7OH_SVz-602u232Xjvde1DAaiePaddIZhDlI6bKITC44aHB-_RvvFQ4_xWseONRAuHhnbdvbdLCOIW7GuAxo1rbx2v3MnqPpkcK8E7hRzcKwjTvjdnzDa8MTOHN_cgUuo-PrCpx9CabCSUGM_AXULTwR1oQzq5tnBD31fzpuymGk8Ya4fuKJolgzgCrHU2bhizXobRjbJoQRCaT8qcG67g11i94hw7qCNeI-asbsrMfq4RUyuqNtSIlmIiglApaqpZWs2nuGpy89U3OGyJNJWswjDACKX6dYEDwcW6kzibZ_uZE30KuzVO5388L4NYHR9ysuTYuiTJoUFKBpFkCWDABm6i2lgnEkAt5hjYQSZM8"
NUCLIA_KB_ID = "17d17844-3acb-4c8f-92bf-1b7aec85b05c"
NUCLIA_API_ENDPOINT = f"https://europe-1.rag.progress.cloud/api/v1/kb/{NUCLIA_KB_ID}/ask"

user_message = "Milyen brókert ajánlasz forex kereskedéshez?"

headers = {
    'Content-Type': 'application/json',
    'X-NUCLIA-SERVICEACCOUNT': f'Bearer {NUCLIA_API_KEY}'
}

payload = {
    'query': user_message,
    'context': []
}

print("Calling Nuclia API...")
response = requests.post(
    NUCLIA_API_ENDPOINT,
    headers=headers,
    json=payload,
    timeout=30
)

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
                        print(f"\nFound retrieval item!")
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
                                print(f"Added citation: {citation_info['title'][:50]}...")
                                
                except json.JSONDecodeError:
                    continue
        
        answer = ''.join(answer_parts) if answer_parts else 'Sajnálom, nem tudok válaszolni erre a kérdésre.'
                
    except Exception as parse_error:
        print(f"Error parsing response: {parse_error}")
        import traceback
        traceback.print_exc()
        answer = 'Sajnálom, nem tudok válaszolni erre a kérdésre.'
    
    print(f"\nAnswer: {answer[:200]}...")
    print(f"\nCitations found: {len(citations)}")
    
    if citations:
        for i, citation in enumerate(citations[:3], 1):
            print(f"\n{i}. {citation['title']}")
            print(f"   Paragraphs: {len(citation['paragraphs'])}")
            if citation['paragraphs']:
                print(f"   First: {citation['paragraphs'][0]['text'][:100]}...")
                
    result = {
        'success': True,
        'message': answer,
        'citations': citations[:5]
    }
    
    print(f"\n\nFinal result structure:")
    print(f"Success: {result['success']}")
    print(f"Message length: {len(result['message'])}")
    print(f"Citations count: {len(result['citations'])}")
    
    # Try to serialize to JSON
    try:
        json_result = json.dumps(result, ensure_ascii=False)
        print(f"\nJSON serialization successful! Length: {len(json_result)}")
    except Exception as e:
        print(f"\nJSON serialization FAILED: {e}")
        import traceback
        traceback.print_exc()
else:
    print(f"Error: {response.status_code}")
    print(response.text)
