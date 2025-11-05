#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test English initialization message
"""
import requests
import json

# Test the init-chat endpoint
url = 'http://127.0.0.1:5000/api/init-chat'

print("Testing init-chat endpoint...")
response = requests.post(url, timeout=30)

if response.status_code == 200:
    data = response.json()
    print(f"\nSuccess: {data.get('success')}")
    print(f"\nWelcome message:\n{data.get('message', '')}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)

print("\n" + "="*80)

# Test a regular chat message
url2 = 'http://127.0.0.1:5000/api/chat'
print("\nTesting chat endpoint with English question...")

response2 = requests.post(
    url2,
    headers={'Content-Type': 'application/json'},
    json={'message': 'What is the best broker for beginners?'},
    timeout=30
)

if response2.status_code == 200:
    data2 = response2.json()
    print(f"\nSuccess: {data2.get('success')}")
    print(f"\nAnswer (first 300 chars):\n{data2.get('message', '')[:300]}...")
    print(f"\nCitations: {len(data2.get('citations', []))} sources found")
else:
    print(f"Error: {response2.status_code}")
    print(response2.text)
