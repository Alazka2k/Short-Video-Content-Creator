import json
import os
import logging
from typing import Dict, Any, Optional
from .prompt_generator import PromptGenerator
from .services import generate_content_with_openai, generate_image, generate_voice, generate_music, generate_video
from .models import Content, db
from .schemas import VideoContent

class ContentCreator:
    def __init__(self, template_file: str, test_input_file: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.prompt_generator = PromptGenerator(template_file)
        self.test_input = self.load_test_input(test_input_file) if test_input_file else None

    def load_test_input(self, test_input_file: str) -> Dict[str, Any]:
        with open(test_input_file, 'r') as file:
            lines = file.readlines()
        inputs = [line.strip() for line in lines]
        return {
            "name": inputs[0],
            "description": inputs[1],
            "target_audience": inputs[2],
            "video_length": int(inputs[3]),
            "image_style": inputs[4],
            "scene_amount": int(inputs[5])
        }

    def create_content(self, input_data: Dict[str, Any], is_test: bool = False) -> Content:
        content = None
        try:
            # Merge input_data with test_input if in test mode
            if is_test and self.test_input:
                merged_input = {**self.test_input, **input_data}
            else:
                merged_input = input_data

            # Remove 'services' from merged_input as it's not used in the template
            services = merged_input.pop('services', None)

            # Generate content prompt
            content_prompt = self.prompt_generator.generate_prompt("video_content", **merged_input)
            
            # Generate content using OpenAI
            generated_content: VideoContent = generate_content_with_openai(content_prompt)

            # Create Content object
            content = Content(
                title=generated_content.video_title,
                description=generated_content.description,
                target_audience=merged_input['target_audience'],
                duration=merged_input['duration'],
                style=merged_input['style'],
                services=json.dumps(services) if services else None,
                generated_content=generated_content.json()
            )
            db.session.add(content)
            db.session.commit()

            return content

        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON: {str(e)}")
            raise Exception(f"Error decoding JSON: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error in content creation pipeline: {str(e)}")
            raise

    def save_debug_info(self, title: str, data: Dict[str, Any]):
        debug_folder = f"debug/content/{title}"
        os.makedirs(debug_folder, exist_ok=True)
        
        with open(f"{debug_folder}/generated_content.json", "w") as f:
            json.dump(data, f, indent=2)

# Make sure to export the class at the end of the file
__all__ = ['ContentCreator']

# Helper function to create content (optional, based on the original code)
def create_content(input_data: Dict[str, Any]) -> Dict[str, Any]:
    creator = ContentCreator("prompt_templates.yaml", "test_input.txt")
    content = creator.create_content(input_data)
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