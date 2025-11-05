#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Translate Hungarian texts to English in brokerchooser.html
"""

# Read the file
with open('/home/ubuntu/_dev/_dominik/bc/hackaton/templates/brokerchooser.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Dictionary of translations
translations = {
    # Main menu items
    'Legjobb brókerek': 'Best Brokers',
    'Bróker értékelések': 'Broker Reviews',
    'Eszközök': 'Tools',
    'Kezdőknek': 'For Beginners',
    'Rólunk': 'About Us',
    
    # CTA Button
    'Találj nekem megfelelőt': 'Find My Broker',
    'Találd meg a brókerem': 'Find My Broker',
    
    # Language
    'Magyar': 'English',
    
    # Main page hero texts
    'Találd meg\\na neked való tesztelve\\nonline brókert': 'Find your\\ntested\\nonline broker',
    
    # Other common texts
    'Személyes oldal': 'Personal Page',
    'Fórum': 'Forum',
    'Profil kezelése': 'Manage Profile',
    'Legjobb brókercégek kategóriánként': 'Best Brokers by Category',
    'Legjobb brókerek kezdőknek': 'Best Brokers for Beginners',
    'Legjobb részvénybrókerek': 'Best Stock Brokers',
    'Legjobb forex brókercégek': 'Best Forex Brokers',
    'Legjobb CFD brókerek': 'Best CFD Brokers',
    'Legjobb opciós brókerek': 'Best Options Brokers',
    'Legjobb határidős brókerek': 'Best Futures Brokers',
    'Legjobb kripto brókercégek': 'Best Crypto Brokers',
    'Minden legjobb rangsor': 'All Best Rankings',
    'Országspecifikus ajánlás': 'Country-Specific Recommendations',
    'Minden értékelés': 'All Reviews',
    'Problémáid megoldva': 'Your Problems Solved',
    'Összes bróker összehasonlítása': 'Compare All Brokers',
    '2 bróker összehasonlítása': 'Compare 2 Brokers',
    'Részvény díj kalkulátor': 'Stock Fee Calculator',
    'Deviza díj kalkulátor': 'Forex Fee Calculator',
    'Csaló bróker védelem': 'Scam Broker Shield',
    'Csaló bróker figyelmeztetés': 'Scam Broker Alert',
    'Tanuld meg az alapokat': 'Learn the Basics',
    'Hosszú távú befektetés': 'Long-Term Investing',
    'Részvénybefektetés': 'Stock Investment',
    'Forex kereskedés': 'Forex Trading',
    'CFD kereskedés': 'CFD Trading',
    'A színfalak mögött': 'Behind the Scenes',
    'A csapat': 'The Team',
    'Módszertanunk': 'Our Methodology',
    'Karrierlehetőségek': 'Career Opportunities',
    'Partnereknek': 'For Partners',
    'Újságíróknak': 'For Journalists',
    'Kapcsolat': 'Contact',
    'Magyarország': 'Hungary',
    'Egyesült Államok': 'United States',
    'Egyesült Királyság': 'United Kingdom',
    'Németország': 'Germany',
    'Hollandia': 'Netherlands',
    'Kanada': 'Canada',
    'Spanyolország': 'Spain',
    'Franciaország': 'France',
    'India': 'India',
    'Ausztrália': 'Australia',
    'Olaszország': 'Italy',
    'További országok': 'More Countries',
    
    # Reviews
    'értékelés': 'review',
    'Az általunk ajánlott brókerek Magyarország-ban/ben': 'Our Recommended Brokers for Hungary',
    
    # Other text
    'Bróker díjak 2025': 'Broker Awards 2025',
    'Legjobb alacsony spread-del rendelkező forex brókercégek': 'Best Low-Spread Forex Brokers',
    'Legjobb brókerek tőkeáttételes kereskedéshez': 'Best Brokers for Margin Trading',
}

# Apply translations
for hu_text, en_text in translations.items():
    content = content.replace(hu_text, en_text)

# Write back
with open('/home/ubuntu/_dev/_dominik/bc/hackaton/templates/brokerchooser.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Translation complete!")
print(f"Applied {len(translations)} translations")
