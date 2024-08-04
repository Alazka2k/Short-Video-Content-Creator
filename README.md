# short-video-content-creator
A script for (semi) automatic short video creation with the help of AI

## Configuration

This project uses a YAML configuration file (`config.yaml`) for general settings and a `.env` file for sensitive information like API keys.

### Setup

1. Copy `config.example.yaml` to `config.yaml` and adjust the settings as needed.
2. Copy `.env.example` to `.env` and fill in your API keys and other sensitive information.

### Usage

The configuration is loaded automatically when you run the application. You can access the configuration in your code like this:

```python
from config_loader import load_config

config = load_config()
api_endpoint = config['api']['claude_ai']

# Prompt Generation System

The Prompt Generation System is a flexible and extensible system for creating prompts for AI models. It uses template files to generate prompts based on input parameters.

## Usage

1. Initialize the PromptGenerator with a template file:
   ```python
   generator = PromptGenerator('path/to/template_file.yaml')