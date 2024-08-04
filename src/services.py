# services.py
import requests
import os
import logging

class MockLLMClient:
    def generate_content(self, prompt):
        logging.info(f"Mock generating content for prompt: {prompt}")
        
        # Generate mock responses based on the prompt
        if "audio script" in prompt.lower():
            return f"This is a mock audio script about {prompt.split('about ')[-1]}. It contains fascinating facts and an engaging narrative."
        elif "scene" in prompt.lower():
            return f"Imagine a scene related to {prompt.split('to ')[-1]}. It's visually striking and emotionally evocative."
        else:
            return f"This is a generic mock response for the prompt: {prompt}"

class LLMClient:
    def __init__(self):
        self.api_key = os.environ.get('ANTHROPIC_API_KEY')
        self.base_url = "https://api.anthropic.com/v1/messages"

    def generate_content(self, prompt):
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.api_key,
        }
        data = {
            "model": "claude-2.1",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300
        }
        
        try:
            logging.info(f"Sending request to Claude API with prompt: {prompt}")
            response = requests.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()  # Raise an exception for bad status codes
            result = response.json()
            logging.info(f"Received response from Claude API: {result}")
            return result['content'][0]['text']
        except requests.exceptions.RequestException as e:
            logging.error(f"API request failed: {e}")
            logging.error(f"Response content: {response.text}")
            return None
        except KeyError as e:
            logging.error(f"Unexpected response format: {e}")
            logging.error(f"Response content: {response.json()}")
            return None

# Choose which client to use
use_mock = os.environ.get('USE_MOCK_LLM', 'false').lower() == 'true'
llm_client = MockLLMClient() if use_mock else LLMClient()