# test_content_creation.py

import sys
import os
from dotenv import load_dotenv

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '.'))
sys.path.insert(0, project_root)

# Load environment variables
load_dotenv(verbose=True)  # Add verbose=True for debugging

# Check if the API key is loaded
api_key = os.environ.get("ANTHROPIC_API_KEY")
if not api_key:
    print("ANTHROPIC_API_KEY not found in environment variables")
    print("Current working directory:", os.getcwd())
    print("Contents of .env file:")
    try:
        with open('.env', 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print(".env file not found")
else:
    print(f"API Key loaded: {api_key[:5]}...{api_key[-5:]}")

from src.workers import content_creation_worker
from src.services import llm_client

def test_content_creation():
    initial_prompt = "Create a short video script"
    run_parameters = {
        "scene_amount": 3,
        "video_length": 60,
        "image_style": "Realistic"
    }
    variable_inputs = {
        "name": "Albert Einstein"
    }

    result = content_creation_worker(initial_prompt, run_parameters, variable_inputs)
    
    print("Content Creation Result:")
    print(result)

def test_llm_api():
    prompt = "Create a short video script about Albert Einstein with 3 scenes, 60 seconds long, in a Realistic style."
    
    response = llm_client.generate_content(prompt)
    
    print("LLM API Response:")
    print(response)

if __name__ == "__main__":
    print("Testing Content Creation:")
    test_content_creation()
    
    print("\nTesting LLM API directly:")
    test_llm_api()