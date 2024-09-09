# backend/src/services.py

from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
from typing import Dict, Any, List
from pydantic import BaseModel
import json
from backend.src.models import VideoContent, Scene
from backend.src.config import load_config
from dataclasses import dataclass

# Load the .env file from the main directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

if not OPENAI_API_KEY:
    logging.error("OPENAI_API_KEY is not set in the environment variables")
    raise ValueError("OPENAI_API_KEY is not set")

# Initialize OpenAI client
client = OpenAI()
config = load_config()

class OpenAIService:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    async def generate_content(self, prompt: str) -> Dict[str, Any]:
        response = await self.client.chat.completions.create(
            model="gpt-4o-2024-08-06",  # Use an available model
            messages=[
                {"role": "system", "content": "You are a creative video content creator. Please provide your response in JSON format."},
                {"role": "user", "content": f"{prompt}\n\nPlease format your response as a JSON object."}
            ],
            response_format={"type": "json_object"},
            temperature=0.7,
        )
        return json.loads(response.choices[0].message.content)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the OpenAI service
openai_service = OpenAIService(api_key=OPENAI_API_KEY)

async def generate_content_with_openai(prompt: str) -> VideoContent:
    try:
        response = await client.chat.completions.create(
            model=config['openai']['model'],  # Uses the model from config.yaml
            messages=[
                {"role": "system", "content": "You are a creative content generator for short videos."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        content_data = json.loads(response.choices[0].message.content)
        return VideoContent(
            video_title=content_data["video_title"],
            description=content_data["description"],
            main_scenes=[Scene(**scene) for scene in content_data["main_scenes"]]
        )
    except Exception as e:
        raise Exception(f"Error in OpenAI API call: {str(e)}")

# Mock implementations for new services
async def generate_image(prompt: str) -> str:
    logging.info(f"Generating image with prompt: {prompt[:50]}...")
    return "http://example.com/generated_image.jpg"

async def generate_voice(script: str) -> str:
    logging.info(f"Generating voice for script: {script[:50]}...")
    return "http://example.com/generated_voice.mp3"

async def generate_music(prompt: str) -> str:
    logging.info(f"Generating music with prompt: {prompt[:50]}...")
    return "http://example.com/generated_music.mp3"

async def generate_video(video_data: Dict[str, Any]) -> str:
    logging.info(f"Generating video with data: {str(video_data)[:100]}...")
    return "http://example.com/generated_video.mp4"

# Ensure all functions are available when imported
__all__ = ['generate_content_with_openai', 'generate_image', 'generate_voice', 'generate_music', 'generate_video', 'OpenAIService', 'Scene', 'VideoContent', 'load_config']