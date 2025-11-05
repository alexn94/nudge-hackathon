# -*- coding: utf-8 -*-
"""
User Journey Analyzer
Analyzes user behavior from BigQuery data and determines use cases for personalized messaging
"""
import pandas as pd
import json
import logging
from datetime import datetime
from bigquery_session_loader import get_session_data

logger = logging.getLogger(__name__)


class UserJourneyAnalyzer:
    """Analyzes user journey based on events and determines use case"""
    
    def __init__(self, session_config_path='session_config.json',
                 prompt_templates_path='prompt_templates.json'):
        """
        Initialize the analyzer
        
        Args:
            session_config_path: Path to session config JSON
            prompt_templates_path: Path to prompt templates JSON
        """
        self.session_config_path = session_config_path
        self.prompt_templates_path = prompt_templates_path
        
        self.df = None
        self.session_id = None
        self.prompt_templates = None
        
    def load_data(self):
        """Load session config and prompt templates"""
        try:
            
            # Load session config
            logger.info(f"Loading session config from {self.session_config_path}")
            with open(self.session_config_path, 'r') as f:
                session_config = json.load(f)
                self.session_id = session_config['session_id']
            logger.info(f"Target session_id: {self.session_id}")
            
            # Load prompt templates
            logger.info(f"Loading prompt templates from {self.prompt_templates_path}")
            with open(self.prompt_templates_path, 'r') as f:
                self.prompt_templates = json.load(f)
            logger.info(f"Loaded {len(self.prompt_templates['use_cases'])} use cases")
            
            return True
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return False
    
    def get_user_events(self):
        """Get all events for the configured session_id from BigQuery"""
        if self.session_id is None:
            logger.error("Session ID not loaded")
            return None
        
        # Query BigQuery directly for this session
        logger.info(f"Fetching events for session_id: {self.session_id}")
        user_data = get_session_data(self.session_id)
        
        if len(user_data) == 0:
            logger.warning(f"No data found for session_id: {self.session_id}")
            return None
        
        # Sort by event_timestamp
        user_data['event_timestamp'] = pd.to_datetime(user_data['event_timestamp'])
        user_data = user_data.sort_values('event_timestamp')
        
        return user_data
    
    def determine_use_case(self, user_data):
        """
        Determine which use case applies based on user events
        
        Args:
            user_data: DataFrame with user events
            
        Returns:
            dict: Use case information
        """
        if user_data is None or len(user_data) == 0:
            return 'new_visitor'
        
        # Get event types
        event_names = user_data['event_name'].unique()
        
        has_registration = 'registration' in event_names
        has_first_deposit = 'first_deposit' in event_names
        has_qualify = 'qualify' in event_names
        
        # Determine use case
        if has_registration and not has_first_deposit and not has_qualify:
            return 'registration_only'
        elif has_registration and has_first_deposit and not has_qualify:
            return 'registration_and_deposit'
        elif has_registration and has_first_deposit and has_qualify:
            return 'full_journey'
        elif has_qualify and not has_registration:
            return 'qualify_only'
        else:
            return 'new_visitor'
    
    def get_user_info(self, user_data):
        """
        Extract user information from the data
        
        Args:
            user_data: DataFrame with user events
            
        Returns:
            dict: User information (name, email, broker_slug)
        """
        if user_data is None or len(user_data) == 0:
            return {}
        
        # Get the most recent record with non-null name
        name_data = user_data[user_data['name'].notna()]
        if len(name_data) > 0:
            name = name_data.iloc[-1]['name']
        else:
            name = None
        
        # Get the most common broker_slug
        broker_slug = user_data['broker_slug'].value_counts().index[0] if len(user_data) > 0 else None
        
        # Get broker_name
        broker_name_data = user_data[user_data['broker_name'].notna()]
        if len(broker_name_data) > 0:
            broker_name = broker_name_data.iloc[-1]['broker_name']
        else:
            broker_name = broker_slug  # Fallback to slug if name not available
        
        # Get email if available
        email_data = user_data[user_data['email'].notna()]
        if len(email_data) > 0:
            email = email_data.iloc[-1]['email']
        else:
            email = None
        
        return {
            'name': name,
            'email': email,
            'broker_slug': broker_slug,
            'broker_name': broker_name
        }
    
    def generate_prompt(self):
        """
        Generate personalized prompt based on user journey
        
        Returns:
            str: Personalized prompt for Nuclia
        """
        # Load data if not already loaded
        if self.df is None:
            if not self.load_data():
                return "Generate a warm welcome message for a visitor to our broker comparison site."
        
        # Get user events
        user_data = self.get_user_events()
        
        # Determine use case
        use_case = self.determine_use_case(user_data)
        logger.info(f"Determined use case: {use_case}")
        
        # Get user info
        user_info = self.get_user_info(user_data)
        logger.info(f"User info: {user_info}")
        
        # Get prompt template
        use_case_config = self.prompt_templates['use_cases'][use_case]
        
        # Choose template based on whether we have a name
        if user_info.get('name'):
            prompt_template = use_case_config['prompt_with_name']
        else:
            prompt_template = use_case_config['prompt_without_name']
        
        # Fill in the template
        prompt = prompt_template.format(
            name=user_info.get('name', ''),
            broker_slug=user_info.get('broker_slug', 'the broker platform')
        )
        
        logger.info(f"Generated prompt: {prompt}")
        return prompt
    
    def generate_welcome_response(self):
        """
        Generate instant welcome message and suggested questions based on user journey
        
        Returns:
            dict: Welcome message and suggested questions
        """
        # Load data if not already loaded
        if self.df is None:
            if not self.load_data():
                return {
                    'message': 'Hi there! 👋 Welcome! Looking for the perfect broker?',
                    'suggested_questions': [
                        '🔍 What are the best brokers for beginners?',
                        '💰 Which brokers have the lowest fees?',
                        '🌍 Which brokers are available in my country?'
                    ]
                }
        
        # Get user events
        user_data = self.get_user_events()
        
        # Determine use case
        use_case = self.determine_use_case(user_data)
        logger.info(f"Determined use case: {use_case}")
        
        # Get user info
        user_info = self.get_user_info(user_data)
        logger.info(f"User info: {user_info}")
        
        # Get use case config
        use_case_config = self.prompt_templates['use_cases'][use_case]
        
        # Choose welcome message based on whether we have a name
        if user_info.get('name'):
            welcome_template = use_case_config['welcome_message_with_name']
        else:
            welcome_template = use_case_config['welcome_message_without_name']
        
        # Fill in the welcome message
        welcome_message = welcome_template.format(
            name=user_info.get('name', ''),
            broker_slug=user_info.get('broker_slug', 'your broker'),
            broker_name=user_info.get('broker_name', 'your broker')
        )
        
        # Fill in the suggested questions
        suggested_questions_template = use_case_config['suggested_questions']
        suggested_questions = [
            q.format(
                broker_slug=user_info.get('broker_slug', 'your broker'),
                broker_name=user_info.get('broker_name', 'your broker')
            ) for q in suggested_questions_template
        ]
        
        logger.info(f"Generated welcome message: {welcome_message}")
        logger.info(f"Generated suggested questions: {suggested_questions}")
        
        return {
            'message': welcome_message,
            'suggested_questions': suggested_questions
        }
    
    def get_analytics_summary(self):
        """
        Get a summary of the user's journey for logging/debugging
        
        Returns:
            dict: Summary information
        """
        if self.df is None:
            self.load_data()
        
        user_data = self.get_user_events()
        
        if user_data is None or len(user_data) == 0:
            return {
                'session_id': self.session_id,
                'found': False,
                'message': 'No data found for this session'
            }
        
        use_case = self.determine_use_case(user_data)
        user_info = self.get_user_info(user_data)
        
        return {
            'session_id': self.session_id,
            'found': True,
            'use_case': use_case,
            'user_info': user_info,
            'event_count': len(user_data),
            'events': user_data['event_name'].value_counts().to_dict(),
            'first_event': user_data.iloc[0]['event_timestamp'].isoformat() if len(user_data) > 0 else None,
            'last_event': user_data.iloc[-1]['event_timestamp'].isoformat() if len(user_data) > 0 else None
        }


# Test function
def test_analyzer():
    """Test the analyzer with current config"""
    analyzer = UserJourneyAnalyzer()
    
    print("="*60)
    print("USER JOURNEY ANALYZER TEST")
    print("="*60)
    
    # Load data
    if not analyzer.load_data():
        print("ERROR: Could not load data")
        return
    
    # Get summary
    summary = analyzer.get_analytics_summary()
    print("\nUser Journey Summary:")
    print(json.dumps(summary, indent=2, default=str))
    
    # Generate prompt
    prompt = analyzer.generate_prompt()
    print("\n" + "="*60)
    print("GENERATED PROMPT:")
    print("="*60)
    print(prompt)
    print("="*60)


if __name__ == '__main__':
    test_analyzer()
