# backend/src/config-loader.py

import os
import yaml
from dotenv import load_dotenv
import logging

load_dotenv()

class ConfigurationError(Exception):
    pass

def load_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, '..', 'config.yaml')
    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    
    # Fügen Sie api_keys zum Config-Objekt hinzu
    config['api_keys'] = get_api_keys()
    return config

def validate_config(config):
    required_sections = ['api', 'content_generation', 'paths', 'logging', 'database', 'features']
    for section in required_sections:
        if section not in config:
            raise ConfigurationError(f"Missing required configuration section: {section}")

    # Überprüfen Sie nur den OPENAI_API_KEY
    openai_api_key = os.getenv('OPENAI_API_KEY')
    if not openai_api_key:
        raise ConfigurationError("Missing OPENAI_API_KEY in environment variables")

    # Überprüfen Sie die Datenbank-URL
    if 'database' not in config or 'url' not in config['database']:
        raise ConfigurationError("Missing database URL in configuration")

def get_api_keys():
    return {
        'openai': os.getenv('OPENAI_API_KEY'),
        'black_forest': os.getenv('BLACK_FOREST_API_KEY', 'N/A'),
        'elevenlabs': os.getenv('ELEVENLABS_API_KEY', 'N/A'),
        'luma': os.getenv('LUMA_API_KEY', 'N/A'),
        'suna': os.getenv('SUNA_API_KEY', 'N/A')
    }

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Debug-Ausgabe
print(f"Config file path: {os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.yaml')}")
print(f"Config file exists: {os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.yaml'))}")