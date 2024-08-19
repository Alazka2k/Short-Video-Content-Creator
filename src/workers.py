import logging
from flask import current_app
from models import db, Content
from services import generate_content_with_openai
from typing import Dict, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PromptGenerator:
    def __init__(self):
        self.templates = {
            "basic": "Create a short video script about {name}. The video should have {scene_amount} scenes.",
            "detailed": "Create a detailed video script about {name}. The video should have {scene_amount} scenes. "
                        "Include information about their background, achievements, and legacy. "
                        "Each scene should be vivid and engaging.",
            "educational": "Create an educational video script about {name} suitable for {target_audience}. "
                           "The video should have {scene_amount} scenes and focus on key facts and interesting details.",
        }

    def generate_prompt(self, template_name: str, variables: Dict[str, Any]) -> str:
        if template_name not in self.templates:
            raise ValueError(f"Unknown template: {template_name}")
        
        template = self.templates[template_name]
        return template.format(**variables)

    def add_template(self, name: str, template: str):
        self.templates[name] = template

prompt_generator = PromptGenerator()

def content_creation_worker(template_name: str, run_parameters: Dict[str, Any], variable_inputs: Dict[str, Any], app=None):
    logging.info(f"Starting content creation for {variable_inputs['name']} using template: {template_name}")
    
    try:
        # Generate the prompt
        full_prompt = prompt_generator.generate_prompt(template_name, {**run_parameters, **variable_inputs})
        
        # Generate content using OpenAI API
        generated_content = generate_content_with_openai(full_prompt)
        
        # Process the generated content
        processed_content = process_generated_content(generated_content, run_parameters)
        
        # Save to database
        if app:
            with app.app_context():
                save_to_database(processed_content, variable_inputs['name'])
        else:
            save_to_database(processed_content, variable_inputs['name'])
        
        return processed_content
    except Exception as e:
        logging.error(f"Error in content creation: {str(e)}")
        return {"error": f"Failed to generate content: {str(e)}"}

def process_generated_content(generated_content: str, run_parameters: Dict[str, Any]) -> Dict[str, Any]:
    # Process the OpenAI's output based on run parameters
    # This is a placeholder implementation. Adjust according to your specific needs.
    scenes = generated_content.split('\n')
    processed_content = {
        'title': scenes[0] if scenes else '',
        'description': scenes[1] if len(scenes) > 1 else '',
        'hashtags': scenes[2] if len(scenes) > 2 else '',
        'opening_scene': scenes[3] if len(scenes) > 3 else '',
        'main_scenes': scenes[4:-1] if len(scenes) > 5 else [],
        'closing_scene': scenes[-1] if scenes else ''
    }
    logging.info(f"Processed content: {processed_content}")
    return processed_content

def save_to_database(processed_content: Dict[str, Any], name: str):
    try:
        content = Content(
            name=name,
            title=processed_content['title'],
            description=processed_content['description'],
            content=str(processed_content)  # Convert dict to string for storage
        )
        db.session.add(content)
        db.session.commit()
        logging.info(f"Saved content to database for {name}")
    except Exception as e:
        logging.error(f"Error saving to database: {str(e)}")
        raise

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# You might want to add any additional setup or initialization code here