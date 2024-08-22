import os
import sys
from dotenv import load_dotenv
from flask import Flask
import json

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(current_dir), 'src')
sys.path.insert(0, src_dir)

from src.app import create_app
from src.workers import content_creation_worker

# Load environment variables
load_dotenv()

# Ensure the OpenAI API key is set
if not os.getenv("OPENAI_API_KEY"):
    print("Error: OPENAI_API_KEY environment variable is not set.")
    sys.exit(1)

# Create a Flask app context
app = create_app()

def get_user_input():
    title = input("Enter the title of the video: ")
    description = input("Enter a brief description: ")
    target_audience = input("Enter the target audience: ")
    duration = int(input("Enter the duration in seconds: "))
    style = input("Enter the style (e.g., informative, entertaining): ")
    scene_amount = int(input("Enter the number of scenes: "))

    services = {
        "contentGeneration": True,
        "imageGeneration": input("Generate images? (y/n): ").lower() == 'y',
        "voiceGeneration": input("Generate voice? (y/n): ").lower() == 'y',
        "musicGeneration": input("Generate music? (y/n): ").lower() == 'y',
        "videoGeneration": input("Generate video? (y/n): ").lower() == 'y'
    }

    return {
        "title": title,
        "description": description,
        "target_audience": target_audience,
        "duration": duration,
        "style": style,
        "scene_amount": scene_amount,
        "services": services
    }

def test_content_creation():
    with app.app_context():
        while True:
            print("\nStarting new content creation test...")
            input_data = get_user_input()

            print(f"\nInput data: {json.dumps(input_data, indent=2)}")

            # Call the content creation worker
            result = content_creation_worker('basic', input_data, [{'name': input_data['title']}], app)

            if result and isinstance(result[0], dict) and 'error' not in result[0]:
                print("\nContent creation successful!")
                print(f"Generated content: {json.dumps(result[0], indent=2)}")
            else:
                error_message = result[0]['error'] if result and isinstance(result[0], dict) else 'Unknown error occurred'
                print(f"\nError in content creation: {error_message}")

            if input("\nDo you want to create another video? (y/n): ").lower() != 'y':
                break

if __name__ == "__main__":
    test_content_creation()