from openai import OpenAI
import os
from dotenv import load_dotenv
import logging
from typing import Dict, Any, List
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

class Scene(BaseModel):
    scene_description: str
    visual_prompt: str

class VideoContent(BaseModel):
    video_title: str
    description: str
    main_scenes: List[Scene]

class OpenAIService:
    def __init__(self):
        self.client = client

    def generate_content(self, prompt: str) -> VideoContent:
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-2024-08-06",
                messages=[
                    {"role": "system", "content": "You are a creative content generator for short videos."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_schema", "schema": VideoContent.schema_json()}
            )
            content = response.choices[0].message.content
            return VideoContent.parse_raw(content)
        except Exception as e:
            logging.error(f"Error in OpenAI API call: {str(e)}")
            raise

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the OpenAI service
openai_service = OpenAIService()

def generate_content_with_openai(prompt: str) -> VideoContent:
    return openai_service.generate_content(prompt)

# Mock implementations for new services
def generate_image(prompt: str) -> str:
    logging.info(f"Generating image with prompt: {prompt[:50]}...")
    return "http://example.com/generated_image.jpg"

def generate_voice(script: str) -> str:
    logging.info(f"Generating voice for script: {script[:50]}...")
    return "http://example.com/generated_voice.mp3"

def generate_music(prompt: str) -> str:
    logging.info(f"Generating music with prompt: {prompt[:50]}...")
    return "http://example.com/generated_music.mp3"

def generate_video(video_data: Dict[str, Any]) -> str:
    logging.info(f"Generating video with data: {str(video_data)[:100]}...")
    return "http://example.com/generated_video.mp4"

# Ensure all functions are available when imported
__all__ = ['generate_content_with_openai', 'generate_image', 'generate_voice', 'generate_music', 'generate_video']