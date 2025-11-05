#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to check Nuclia citations
"""
import requests
import json

NUCLIA_API_KEY = "eyJhbGciOiJSUzI1NiIsImtpZCI6InNhIiwidHlwIjoiSldUIn0.eyJpc3MiOiJodHRwczovL2V1cm9wZS0xLm51Y2xpYS5jbG91ZC8iLCJpYXQiOjE3NjIxODM1NTAsInN1YiI6IjQ1MTE0ZTFmLTZkZmEtNDkwZC1iN2ZkLWVkYmJjMmZhNTc5YSIsImp0aSI6IjJjMGIxOGNmLWM1ZjgtNGZjNi04ODVjLTdlZDNhZDQwZGZiNCIsImV4cCI6MTc5MzcxOTU0OSwia2V5IjoiYWY2ODYwMDAtMzQ4Zi00NWUwLTgzMGItOTI5MThlNTAxZjUyIiwia2lkIjoiMjg4NzdlOTgtZWZlMC00YjM2LWIyYjctN2I4YWQ2MTdmZTE4In0.geM880M25Nj_z-ds3uvd2CxyPbEBAU0xq-sy_oscoWGDlCNLYbndA9FgLthuugN_I6HyQOUIzUvZwE_crnKNireA8tRgki-2Y27AMa7-N0VRS1HLKJaYvJCmLOqlY-2hT3xWdsLI2ZIR05fbY3cc1oosr4wK5UDGluTf9vt88sqCsrrySvsrJ07PTaDA5eKpNq0F9jwvIjNOj4lj9dyu0jOAIz2mPSoPu_OCuDwYdBnywKdmsTP_CoBeDFNqHFR_A6HBUkyQzXWa9vMnGAUzS9rHVlE6VzM0fPa4LeizPoPrnhKCwur6alKEl22PheDl7OH_SVz-602u232Xjvde1DAaiePaddIZhDlI6bKITC44aHB-_RvvFQ4_xWseONRAuHhnbdvbdLCOIW7GuAxo1rbx2v3MnqPpkcK8E7hRzcKwjTvjdnzDa8MTOHN_cgUuo-PrCpx9CabCSUGM_AXULTwR1oQzq5tnBD31fzpuymGk8Ya4fuKJolgzgCrHU2bhizXobRjbJoQRCaT8qcG67g11i94hw7qCNeI-asbsrMfq4RUyuqNtSIlmIiglApaqpZWs2nuGpy89U3OGyJNJWswjDACKX6dYEDwcW6kzibZ_uZE30KuzVO5388L4NYHR9ysuTYuiTJoUFKBpFkCWDABm6i2lgnEkAt5hjYQSZM8"
NUCLIA_KB_ID = "17d17844-3acb-4c8f-92bf-1b7aec85b05c"
NUCLIA_API_ENDPOINT = f"https://europe-1.rag.progress.cloud/api/v1/kb/{NUCLIA_KB_ID}/ask"

# Test queries
test_queries = [
    "Milyen szolgáltatásokat kínál a BrokerChooser?",
    "Mi a BrokerChooser?",
    "Hogyan működik a platform?"
]

def test_query(query):
    print(f"\n{'='*80}")
    print(f"Testing query: {query}")
    print('='*80)
    
    headers = {
        'Content-Type': 'application/json',
        'X-NUCLIA-SERVICEACCOUNT': f'Bearer {NUCLIA_API_KEY}'
    }
    
    payload = {
        'query': query,
        'context': []
    }
    
    try:
        response = requests.post(
            NUCLIA_API_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        response.encoding = 'utf-8'
        
        if response.status_code == 200:
            response_text = response.text
            lines = response_text.strip().split('\n')
            
            print(f"\nReceived {len(lines)} lines in response\n")
            
            for i, line in enumerate(lines):
                if line.strip():
                    try:
                        line_data = json.loads(line)
                        print(f"Line {i+1}:")
                        print(f"  Type: {line_data.get('item', {}).get('type', 'unknown')}")
                        print(f"  Full data: {json.dumps(line_data, indent=2, ensure_ascii=False)}")
                        print()
                    except json.JSONDecodeError as e:
                        print(f"Line {i+1}: Failed to parse JSON - {e}")
                        print(f"  Raw line: {line}")
                        print()
        else:
            print(f"Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Exception: {str(e)}")

if __name__ == '__main__':
    for query in test_queries:
        test_query(query)
        print("\n" + "="*80 + "\n")
