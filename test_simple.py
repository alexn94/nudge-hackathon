#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple test for Nuclia citations
"""
import requests
import json

NUCLIA_API_KEY = "eyJhbGciOiJSUzI1NiIsImtpZCI6InNhIiwidHlwIjoiSldUIn0.eyJpc3MiOiJodHRwczovL2V1cm9wZS0xLm51Y2xpYS5jbG91ZC8iLCJpYXQiOjE3NjIxODM1NTAsInN1YiI6IjQ1MTE0ZTFmLTZkZmEtNDkwZC1iN2ZkLWVkYmJjMmZhNTc5YSIsImp0aSI6IjJjMGIxOGNmLWM1ZjgtNGZjNi04ODVjLTdlZDNhZDQwZGZiNCIsImV4cCI6MTc5MzcxOTU0OSwia2V5IjoiYWY2ODYwMDAtMzQ4Zi00NWUwLTgzMGItOTI5MThlNTAxZjUyIiwia2lkIjoiMjg4NzdlOTgtZWZlMC00YjM2LWIyYjctN2I4YWQ2MTdmZTE4In0.geM880M25Nj_z-ds3uvd2CxyPbEBAU0xq-sy_oscoWGDlCNLYbndA9FgLthuugN_I6HyQOUIzUvZwE_crnKNireA8tRgki-2Y27AMa7-N0VRS1HLKJaYvJCmLOqlY-2hT3xWdsLI2ZIR05fbY3cc1oosr4wK5UDGluTf9vt88sqCsrrySvsrJ07PTaDA5eKpNq0F9jwvIjNOj4lj9dyu0jOAIz2mPSoPu_OCuDwYdBnywKdmsTP_CoBeDFNqHFR_A6HBUkyQzXWa9vMnGAUzS9rHVlE6VzM0fPa4LeizPoPrnhKCwur6alKEl22PheDl7OH_SVz-602u232Xjvde1DAaiePaddIZhDlI6bKITC44aHB-_RvvFQ4_xWseONRAuHhnbdvbdLCOIW7GuAxo1rbx2v3MnqPpkcK8E7hRzcKwjTvjdnzDa8MTOHN_cgUuo-PrCpx9CabCSUGM_AXULTwR1oQzq5tnBD31fzpuymGk8Ya4fuKJolgzgCrHU2bhizXobRjbJoQRCaT8qcG67g11i94hw7qCNeI-asbsrMfq4RUyuqNtSIlmIiglApaqpZWs2nuGpy89U3OGyJNJWswjDACKX6dYEDwcW6kzibZ_uZE30KuzVO5388L4NYHR9ysuTYuiTJoUFKBpFkCWDABm6i2lgnEkAt5hjYQSZM8"
NUCLIA_KB_ID = "17d17844-3acb-4c8f-92bf-1b7aec85b05c"
NUCLIA_API_ENDPOINT = f"https://europe-1.rag.progress.cloud/api/v1/kb/{NUCLIA_KB_ID}/ask"

headers = {
    'Content-Type': 'application/json',
    'X-NUCLIA-SERVICEACCOUNT': f'Bearer {NUCLIA_API_KEY}'
}

payload = {
    'query': "Mi a BrokerChooser?",
    'context': []
}

print("Sending request to Nuclia...")
response = requests.post(
    NUCLIA_API_ENDPOINT,
    headers=headers,
    json=payload,
    timeout=30
)

print(f"Status: {response.status_code}\n")

if response.status_code == 200:
    lines = response.text.strip().split('\n')
    print(f"Got {len(lines)} lines\n")
    
    for i, line in enumerate(lines, 1):
        if line.strip():
            try:
                data = json.loads(line)
                item = data.get('item', {})
                item_type = item.get('type', 'unknown')
                
                print(f"--- Line {i} (Type: {item_type}) ---")
                
                if item_type == 'answer':
                    print(f"Text: {item.get('text', '')[:100]}...")
                elif item_type == 'citations':
                    print(f"Citations data: {json.dumps(item, indent=2, ensure_ascii=False)}")
                else:
                    print(f"Full item: {json.dumps(item, indent=2, ensure_ascii=False)}")
                print()
                
            except json.JSONDecodeError as e:
                print(f"Line {i}: Parse error - {e}")
else:
    print(f"Error: {response.text}")
