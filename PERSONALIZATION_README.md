# Personalized Nuri Chat - User Journey Based Messaging

## Overview
This system provides personalized welcome messages in the Nuri chat widget based on user behavior tracked in BigQuery. The system analyzes user journey stages and generates tailored prompts for different scenarios.

## How It Works

### 1. **Data Flow**
```
BigQuery → CSV Download → User Journey Analysis → Personalized Prompt → Nuclia AI → User
```

### 2. **Startup Process**
When you run `python3 app.py`, the system:
1. **Refreshes BigQuery data** - Downloads latest user event data (10,000 rows)
2. **Initializes analyzer** - Loads session config and prompt templates
3. **Starts Flask app** - Serves the BrokerChooser website with personalized Nuri chat

### 3. **Components**

#### **Configuration Files**

##### `session_config.json`
Configure which user session to track:
```json
{
  "session_id": 192867611.0,
  "description": "Configure which session_id to track for personalized Nuri chat messages"
}
```

##### `prompt_templates.json`
Defines prompt templates for different user journey stages (use cases):
- **registration_only** - User registered but no first deposit
- **registration_and_deposit** - User registered and deposited but not trading
- **full_journey** - User completed registration, deposit, and is actively trading
- **qualify_only** - User is trading but no clear registration event
- **new_visitor** - No events found for this session

Each use case has two variants:
- `prompt_with_name` - Used when user's name is available
- `prompt_without_name` - Used when name is not available

#### **Core Modules**

##### `user_journey_analyzer.py`
Analyzes user behavior and generates personalized prompts:
- Loads BigQuery CSV data
- Filters data by session_id
- Determines user journey stage (use case)
- Extracts user information (name, email, broker_slug)
- Generates appropriate prompt based on journey stage

##### `app.py` (Modified)
Flask application with personalization:
- Refreshes BigQuery data on startup
- Initializes user journey analyzer
- `/api/init-chat` endpoint uses personalized prompts instead of hardcoded messages

##### `database_access/download_and_load_bigquery.py` (Modified)
Downloads user data with JOIN queries:
```sql
WITH e2e_conversions_users as (
  SELECT 
      eb.*,
      ec.session_id,
      u.id as user_id,
      u.name,
      u.email
  FROM e2e_brokers_log eb
  LEFT JOIN e2e_conversions ec ON eb.e2e_conversions_id = ec.id
  LEFT JOIN sessions s ON ec.session_id = s.id
  LEFT JOIN users u ON s.user_id = u.id
)
```

## Usage

### 1. **Configure Session ID**
Edit `session_config.json` to track a specific user:
```json
{
  "session_id": 213965021.0
}
```

### 2. **Run the Application**
```bash
python3 app.py
```

The app will:
- Download fresh data from BigQuery
- Analyze the configured session
- Start the Flask server at `http://localhost:5000`

### 3. **Test the Analyzer**
You can test the analyzer independently:
```bash
python3 user_journey_analyzer.py
```

This will show:
- User journey summary
- Detected use case
- Generated personalized prompt

### 4. **View Results**
Open `http://localhost:5000` in your browser. The Nuri chat widget will display a personalized welcome message based on the user's journey.

## Use Case Examples

### Example 1: User with Registration Only
**Session ID:** 192867611.0  
**Name:** Camara Abdoulaye  
**Broker:** fusion-markets  
**Events:** registration (2x)  

**Generated Prompt:**
> "Greet Camara Abdoulaye warmly in English. Remind them that they registered on fusion-markets but haven't made their first deposit yet. Explain that to keep their account active, they need to make a deposit. Be friendly, personal, and motivating."

**Nuri Response:** Personalized message encouraging Camara to complete the deposit.

### Example 2: Full Journey User (No Name)
**Session ID:** 213965021.0  
**Name:** N/A  
**Broker:** ig  
**Events:** registration, first_deposit, qualify (2x)  

**Generated Prompt:**
> "Greet the user warmly in English. Congratulate them for being an active trader on ig. Thank them for their engagement and offer assistance with any questions they might have. Be warm and professional."

**Nuri Response:** Congratulatory message for active traders.

## Data Schema

The BigQuery CSV contains these columns:
- `e2e_conversions_id` - Conversion event ID
- `broker_slug` - Broker identifier (e.g., "fusion-markets", "ig", "pepperstone")
- `event_name` - Event type: "registration", "first_deposit", "qualify"
- `event_value` - Numeric value associated with event
- `event_timestamp` - When the event occurred
- `updated_at` - When the record was last updated
- `session_id` - Session identifier (key for tracking users)
- `user_id` - User ID from users table
- `name` - User's name (if available)
- `email` - User's email (if available)

## Customization

### Adding New Use Cases
Edit `prompt_templates.json`:
```json
"my_custom_case": {
  "description": "Description of this use case",
  "conditions": {
    "has_registration": true,
    "has_custom_event": true
  },
  "prompt_with_name": "Your prompt with {name} and {broker_slug}",
  "prompt_without_name": "Your prompt with {broker_slug}"
}
```

Then update `user_journey_analyzer.py` in the `determine_use_case()` method to detect your new case.

### Modifying Prompt Style
All prompts should follow this format:
- Start with: "Greet [name/user] warmly in English."
- Use direct instructions: "Remind them...", "Explain that...", "Encourage them..."
- Avoid meta-instructions like "Generate a message..."
- Keep it concise and actionable

## Files Modified/Created

### New Files
- `session_config.json` - Session tracking configuration
- `prompt_templates.json` - Prompt templates for all use cases
- `user_journey_analyzer.py` - User journey analysis logic
- `PERSONALIZATION_README.md` - This documentation

### Modified Files
- `app.py` - Added BigQuery refresh and personalization logic
- `database_access/download_and_load_bigquery.py` - Updated SQL query to include user data
- `.gitignore` - Allowed config JSONs and CSV data

## Troubleshooting

### Issue: "No data found for session_id"
**Solution:** Check that the session_id exists in the BigQuery data:
```bash
grep "session_id_value" database_access/bigquery_data.csv
```

### Issue: "I'm sorry, I can't answer in that format"
**Solution:** This means the Nuclia API doesn't like the prompt format. Ensure prompts:
- Use direct instructions (Greet, Remind, Explain)
- Avoid "Generate a message..." patterns
- Are concise and clear

### Issue: BigQuery refresh fails
**Solution:** 
1. Check credentials file exists: `database_access/affable-album-354309-72260dd4d800.json`
2. Verify BigQuery permissions
3. Check network connectivity

## Performance Notes

- BigQuery refresh takes ~10-30 seconds on startup
- 10,000 rows are downloaded (configurable in `download_and_load_bigquery.py`)
- Data is cached in CSV until next app restart
- Session analysis is instantaneous (<1ms)

## Future Enhancements

- [ ] Add more granular use cases (e.g., deposit amount thresholds)
- [ ] Track user journey in real-time (websocket integration)
- [ ] A/B testing different prompt styles
- [ ] Multi-language support
- [ ] Automatic session_id detection from frontend
- [ ] Dashboard for monitoring use case distribution
