# BrokerChooser Flask App - Nuclia AI Integration

Ez egy Flask-alapú webalkalmazás, amely a BrokerChooser oldal offline verzióját jeleníti meg Nuclia AI chatbot integrációval.

## Főbb Funkciók

- 🎨 **BrokerChooser-szerű design**: Modern, professzionális megjelenés
- 🤖 **Nuclia AI chatbot**: Intelligens asszisztens, amely válaszol a bróker-választással kapcsolatos kérdésekre
- ⚡ **Automatikus inicializálás**: A chatbot 2.5 másodperc után automatikusan üzenetet küld
- 💬 **Valós idejű kommunikáció**: A Nuclia API segítségével intelligens válaszokat ad
- 🔄 **Session-független**: Minden oldalbetöltés után újraindul a chat

## Projekt Struktúra

```
/hackaton
  ├── app.py                 # Flask backend alkalmazás
  ├── requirements.txt       # Python függőségek
  ├── README.md             # Dokumentáció
  ├── /static
  │   ├── /css
  │   │   └── style.css     # BrokerChooser-szerű stílusok
  │   ├── /js
  │   │   └── chat.js       # Nuclia chat funkcionalitás
  │   └── /images           # Képek helye (később)
  └── /templates
      └── index.html        # Főoldal template
```

## Telepítés és Futtatás

### 1. Függőségek telepítése

```bash
cd /home/ubuntu/_dev/_dominik/bc/hackaton
pip install -r requirements.txt
```

### 2. Alkalmazás indítása

```bash
python app.py
```

Az alkalmazás elérhető lesz: `http://localhost:5000`

## Nuclia API Integráció

### Konfiguráció

- **Knowledge Base ID**: `17d17844-3acb-4c8f-92bf-1b7aec85b05c`
- **API Endpoint**: `https://europe-1.rag.progress.cloud/api/v1/kb/17d17844-3acb-4c8f-92bf-1b7aec85b05c/ask`
- **Reader API Key**: Beépítve az `app.py` fájlba

### Működés

1. **Automatikus inicializálás**: Az oldal betöltése után 2.5 másodperc múlva a chatbot automatikusan üzenetet küld
2. **Előre beállított prompt**: "A felhasználó érdeklődött az Interactive Brokers (IBKR) után..."
3. **Nuclia válasz**: A Nuclia AI a vektorizált adatok és production prompt alapján válaszol
4. **Chat widget**: Jobb alsó sarokban jelenik meg 3 másodperces késleltetéssel

## API Endpointok

### GET /
- Főoldal megjelenítése

### POST /api/chat
- Felhasználói üzenet küldése a Nuclia AI-hoz
- Request body: `{"message": "user message"}`
- Response: `{"success": true, "message": "AI response"}`

### POST /api/init-chat
- Automatikus chatbot inicializálás
- Előre definiált prompt-tal hívja a Nuclia API-t
- Response: `{"success": true, "message": "AI greeting"}`

## Technológiai Stack

- **Backend**: Flask 3.0.0
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **AI**: Nuclia RAG (Retrieval Augmented Generation)
- **HTTP Client**: Python Requests

## Fejlesztési Megjegyzések

- A chatbot nem tárol előzményeket, minden oldalbetöltés tiszta lappal indul
- A Nuclia API válaszideje változó lehet (általában 2-5 másodperc)
- A design teljesen responzív, mobilon is jól használható
- Nincs szükség internet kapcsolatra az assets betöltéséhez (minden local)

## Biztonsági Megjegyzések

⚠️ **FONTOS**: Az API kulcs jelenleg a kódban van tárolva. Production környezetben használj környezeti változókat!

```python
# .env fájlban:
NUCLIA_API_KEY=your_api_key_here

# app.py-ban:
import os
NUCLIA_API_KEY = os.getenv('NUCLIA_API_KEY')
```

## Hibakeresés

### Chat nem jelenik meg
- Ellenőrizd a böngésző konzolt (F12)
- Nézd meg a Flask log-okat

### Nuclia API hiba
- Ellenőrizd az API kulcs érvényességét
- Nézd meg a Knowledge Base ID helyességét
- Próbáld meg közvetlenül curl-lel is tesztelni

### Styling problémák
- Hard refresh (Ctrl+Shift+R)
- Töröld a böngésző cache-t

## Licenc

Ez egy hackathon projekt, demonstration célokra.

## Kapcsolat

Ha kérdésed van, vedd fel a kapcsolatot a fejlesztővel!
