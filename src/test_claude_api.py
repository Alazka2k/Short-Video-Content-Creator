# test_claude_api.py
import os
from dotenv import load_dotenv
from services import LLMClient

# Load environment variables
load_dotenv()

def main():
    # Create an instance of LLMClient
    client = LLMClient()

    # Test the connection
    print("Testing connection to Claude API...")
    if client.test_connection():
        print("Connection successful!")
    else:
        print("Connection failed. Please check your API key and internet connection.")
        return

    # Test content generation
    print("\nTesting content generation...")
    prompt = "Tell me a short joke about programming."
    response = client.generate_content(prompt)
    
    if response:
        print(f"Generated content:\n{response}")
    else:
        print("Failed to generate content. Please check the logs for more information.")

if __name__ == "__main__":
    main()