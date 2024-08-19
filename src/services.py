from openai import OpenAI
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_content_with_openai(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # Make sure this model name is correct
            messages=[
                {"role": "system", "content": "You are a creative content generator for short videos."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000  # Adjust as needed
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error in OpenAI API call: {str(e)}")
        raise

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ensure the function is available when imported
__all__ = ['generate_content_with_openai']