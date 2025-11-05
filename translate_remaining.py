#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix remaining Hungarian texts and translation errors
"""

# Read the file
with open('/home/ubuntu/_dev/_dominik/bc/hackaton/templates/brokerchooser.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix remaining translations
remaining_fixes = {
    'Best Brokers kezdőknek': 'Best Brokers for Beginners',
    'Best Brokers tőkeáttételes kereskedéshez': 'Best Brokers for Margin Trading',
    'Englishország': 'Hungary',
    'Az általunk ajánlott brókerek Englishország-ban/ben': 'Our Recommended Brokers for Hungary',
    'kezdőknek': 'for beginners',
}

# Apply fixes
for old, new in remaining_fixes.items():
    content = content.replace(old, new)

# Write back
with open('/home/ubuntu/_dev/_dominik/bc/hackaton/templates/brokerchooser.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Remaining translations fixed!")
print(f"Applied {len(remaining_fixes)} fixes")
