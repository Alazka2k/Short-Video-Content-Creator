import os
import yaml
from dotenv import load_dotenv

class ConfigurationError(Exception):
    pass

def load_config():
    # Load .env file
    load_dotenv()

    # Determine which config file to use
    config_path = os.getenv('CONFIG_PATH', 'config.yaml')

    # Load YAML configuration
    try:
        with open(config_path, 'r') as config_file:
            config = yaml.safe_load(config_file)
    except FileNotFoundError:
        raise ConfigurationError(f"Configuration file not found: {config_path}")
    except yaml.YAMLError as e:
        raise ConfigurationError(f"Error parsing YAML configuration: {e}")

    # Override with environment variables
    for section, settings in config.items():
        if isinstance(settings, dict):
            for key, value in settings.items():
                env_var = f"{section.upper()}_{key.upper()}"
                env_value = os.getenv(env_var)
                if env_value is not None:
                    # Convert environment variable to appropriate type
                    if isinstance(value, bool):
                        config[section][key] = env_value.lower() in ('true', '1', 'yes')
                    elif isinstance(value, int):
                        config[section][key] = int(env_value)
                    elif isinstance(value, float):
                        config[section][key] = float(env_value)
                    else:
                        config[section][key] = env_value

    # Add API keys from .env
    config['api_keys'] = {
        'anthropic': os.getenv('ANTHROPIC_API_KEY'),
        'black_forest': os.getenv('BLACK_FOREST_API_KEY'),
        'elevenlabs': os.getenv('ELEVENLABS_API_KEY'),
        'luma': os.getenv('LUMA_API_KEY'),
        'suna': os.getenv('SUNA_API_KEY'),
    }

    # Validate configuration
    validate_config(config)

    return config

def validate_config(config):
    required_sections = ['api', 'content_generation', 'paths', 'logging', 'database', 'features']
    for section in required_sections:
        if section not in config:
            raise ConfigurationError(f"Missing required configuration section: {section}")

    # Check for required API keys
    required_api_keys = ['anthropic', 'black_forest', 'elevenlabs', 'luma', 'suna']
    for key in required_api_keys:
        if not config['api_keys'].get(key):
            raise ConfigurationError(f"Missing required API key: {key}")

    # Validate content generation settings
    content_gen = config.get('content_generation', {})
    if not isinstance(content_gen.get('scene_amount'), int) or content_gen.get('scene_amount') <= 0:
        raise ConfigurationError("Invalid 'scene_amount' in content_generation")

    # Validate paths
    for path_key in ['input_directory', 'output_directory', 'logs_directory']:
        if not config['paths'].get(path_key):
            raise ConfigurationError(f"Missing required path: {path_key}")

    # Validate logging settings
    log_config = config.get('logging', {})
    if log_config.get('level') not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
        raise ConfigurationError("Invalid logging level")

    # Validate database URL
    if not config['database'].get('url'):
        raise ConfigurationError("Missing da