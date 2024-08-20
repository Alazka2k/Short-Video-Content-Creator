from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
from typing import Dict, Any
import json

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class OpenAIService:
    def __init__(self):
        self.client = client

    def generate_content(self, prompt: str, max_tokens: int = 1000) -> Dict[str, Any]:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a creative content generator for short videos."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens
            )
            content = response.choices[0].message.content
            return self._parse_content(content)
        except Exception as e:
            logging.error(f"Error in OpenAI API call: {str(e)}")
            raise

    def _parse_content(self, content: str) -> Dict[str, Any]:
        try:
            # Attempt to parse the content as JSON
            return json.loads(content)
        except json.JSONDecodeError:
            # If parsing fails, return the content as a string in a dictionary
            return {"raw_content": content}

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the OpenAI service
openai_service = OpenAIService()

def generate_content_with_openai(prompt: str) -> Dict[str, Any]:
    return openai_service.generate_content(prompt)

# Ensure the function is available when imported
__all__ = ['generate_content_with_openai']