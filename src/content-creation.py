import json
import os
import logging
from typing import Dict, Any
from prompt_generator import PromptGenerator
from services import generate_content_with_openai, generate_image, generate_voice, generate_music, generate_video
from models import Content, db

class ContentCreationPipeline:
    def __init__(self, template_file: str):
        self.logger = logging.getLogger(__name__)
        self.prompt_generator = PromptGenerator(template_file)

    def create_content(self, input_data: Dict[str, Any]) -> Content:
        try:
            # Generate prompt and content
            prompt = self.prompt_generator.generate_prompt("video_content", input_data)
            generated_content = generate_content_with_openai(prompt)

            # Create Content object
            content = Content(
                title=input_data['title'],
                description=input_data['description'],
                target_audience=input_data['target_audience'],
                duration=input_data['duration'],
                style=input_data['style'],
                services=json.dumps(input_data['services']),
                generated_content=json.dumps(generated_content)
            )

            # Generate additional content if services are selected
            if input_data['services'].get('imageGeneration'):
                content.generated_picture = generate_image(generated_content['visual_prompt'])
            
            if input_data['services'].get('voiceGeneration'):
                content.generated_voice = generate_voice(generated_content['audio_narration'])
            
            if input_data['services'].get('musicGeneration'):
                content.generated_music = generate_music(input_data['style'])
            
            if input_data['services'].get('videoGeneration'):
                video_data = {
                    'images': [content.generated_picture],
                    'audio': [content.generated_voice, content.generated_music],
                    'script': generated_content['video_content']
                }
                content.generated_video = generate_video(video_data)

            # Save to database
            db.session.add(content)
            db.session.commit()

            self.save_debug_info(input_data['title'], generated_content)
            
            return content

        except Exception as e:
            self.logger.error(f"Error in content creation pipeline: {str(e)}")
            raise

    def save_debug_info(self, title: str, data: Dict[str, Any]):
        debug_folder = f"debug/content/{title}"
        os.makedirs(debug_folder, exist_ok=True)
        
        with open(f"{debug_folder}/generated_content.json", "w") as f:
            json.dump(data, f, indent=2)

def create_content(input_data: Dict[str, Any]) -> Dict[str, Any]:
    pipeline = ContentCreationPipeline("prompt_templates.yaml")
    content = pipeline.create_content(input_data)
    return content.to_dict()

if __name__ == "__main__":
    # Example usage
    input_data = {
        "title": "The Life of Albert Einstein",
        "description": "A short video about the life and achievements of Albert Einstein",
        "target_audience": "Science enthusiasts, ages 18-50",
        "duration": 120,
        "style": "informative",
        "services": {
            "contentGeneration": True,
            "imageGeneration": True,
            "voiceGeneration": True,
            "musicGeneration": False,
            "videoGeneration": True
        },
        "name": "Albert Einstein",
        "scene_amount": 3,
        "video_length": 120,
        "image_style": "realistic"
    }
    
    result = create_content(input_data)
    print(json.dumps(result, indent=2))