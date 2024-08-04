# src/services.py

import os
import logging
from anthropic import Anthropic

class LLMClient:
    def __init__(self):
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("Warning: ANTHROPIC_API_KEY not found in environment variables")
            api_key = input("Please enter your Anthropic API key: ").strip()
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-3-5-sonnet-20240620"

class MockLLMClient:
    def generate_content(self, prompt):
        logging.info(f"Mock generating content for prompt: {prompt}")
        
        if "audio script" in prompt.lower():
            return f"This is a mock audio script about {prompt.split('about ')[-1]}. It contains fascinating facts and an engaging narrative."
        elif "scene" in prompt.lower():
            return f"Imagine a scene related to {prompt.split('to ')[-1]}. It's visually striking and emotionally evocative."
        else:
            return f"This is a generic mock response for the prompt: {prompt}"

# Use environment variable to determine whether to use mock or real client
use_mock = os.environ.get('USE_MOCK_LLM', 'false').lower() == 'true'
llm_client = MockLLMClient() if use_mock else LLMClient()