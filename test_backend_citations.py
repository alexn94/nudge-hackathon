#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test backend to verify citations are returned
"""
import requests
import json

# Test the local Flask API
url = 'http://127.0.0.1:5000/api/chat'

test_questions = [
    "Mi a BrokerChooser?",
    "Milyen szolgáltatásokat kínál a platform?",
    "Hogyan működik a brókervá lasztó?"
]

for question in test_questions:
    print(f"\n{'='*80}")
    print(f"Testing: {question}")
    print('='*80)
    
    response = requests.post(
        url,
        headers={'Content-Type': 'application/json'},
        json={'message': question},
        timeout=30
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nSuccess: {data.get('success')}")
        print(f"\nAnswer (first 200 chars): {data.get('message', '')[:200]}...")
        
        citations = data.get('citations', [])
        print(f"\nCitations found: {len(citations)}")
        
        if citations:
            print("\nCitations details:")
            for i, citation in enumerate(citations, 1):
                print(f"\n  {i}. {citation.get('title', 'N/A')}")
                print(f"     Paragraphs: {len(citation.get('paragraphs', []))}")
                if citation.get('paragraphs'):
                    print(f"     First paragraph (100 chars): {citation['paragraphs'][0].get('text', '')[:100]}...")
    else:
        print(f"Error: {response.status_code}")
        print(response.text)

print("\n" + "="*80)
print("Testing complete!")
