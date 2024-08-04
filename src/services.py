# services.py
import os
import logging
from anthropic import Anthropic
from tenacity import retry, stop_after_attempt, wait_exponential

class LLMClient:
    def __init__(self):
        self.client = Anthropic()
        self.model = "claude-3-5-sonnet-20240620"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def generate_content(self, prompt):
        """Generate content using the Claude API with retry mechanism."""
        try:
            logging.info(f"Sending request to Claude API with prompt: {prompt}")
            response = self.client.completions.create(
                model=self.model,
                max_tokens_to_sample=1000,
                prompt=f"Human: {prompt}\n\nAssistant:",
            )
            logging.info(f"Received response from Claude API")
            return response.completion
        except Exception as e:
            logging.error(f"API request failed: {e}")
            raise  # Re-raise the exception to trigger a retry

class MockLLMClient:
    def generate_content(self, prompt):
        logging.info(f"Mock generating content for prompt: {prompt}")
        
        if "audio script" in prompt.lower():
            return f"This is a mock audio script about {prompt.split('about ')[-1]}. It contains fascinating facts and an engaging narrative."
        elif "scene" in prompt.lower():
            return f"Imagine a scene related to {prompt.split('to ')[-1]}. It's visually striking and emotionally evocative."
        else:
            return f"This is a generic mock response for the prompt: {prompt}"

# Choose which client to use
use_mock = os.environ.get('USE_MOCK_LLM', 'false').lower() == 'true'
llm_client = MockLLMClient() if use_mock else LLMClient()