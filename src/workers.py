import logging
from flask import current_app
from .models import db, Content
from .services import generate_content_with_openai, generate_image, generate_voice, generate_music, generate_video, VideoContent
from typing import Dict, Any, List
import os
from dotenv import load_dotenv
import csv
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from .progress_tracker import ProgressTracker

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

class ContentCreationPipeline:
    def __init__(self):
        self.prompt_generator = PromptGenerator()
        self.logger = logging.getLogger(__name__)

    def process_input(self, input_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        total_entries = len(input_data)
        progress_tracker = ProgressTracker(total_entries * 6)  # 6 steps per entry

        with ThreadPoolExecutor() as executor:
            future_to_entry = {executor.submit(self.create_content, entry, index, total_entries, progress_tracker): entry for index, entry in enumerate(input_data, start=1)}
            for future in as_completed(future_to_entry):
                entry = future_to_entry[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    self.logger.error(f"Error processing entry: {entry['name']} - {str(e)}", exc_info=True)
                    results.append({"error": str(e), "name": entry['name']})

        return results

    def create_content(self, input_data: Dict[str, Any], index: int, total_entries: int, progress_tracker: ProgressTracker) -> Dict[str, Any]:
        self.logger.info(f"Processing entry {index}/{total_entries}: {input_data['name']}")
        base_step = (index - 1) * 6
        try:
            template_name = input_data.get('template', 'basic')
            prompt = self.prompt_generator.generate_prompt(template_name, input_data)
            generated_content: VideoContent = generate_content_with_openai(prompt)
            progress_tracker.update(base_step + 1, {"name": input_data['name'], "status": "content generated"})

            processed_content = self.process_generated_content(generated_content, input_data)
            progress_tracker.update(base_step + 2, {"name": input_data['name'], "status": "content processed"})
            
            # Generate additional content based on selected services
            if input_data.get('generate_image'):
                processed_content['image_url'] = self.generate_image_content(processed_content['description'])
                progress_tracker.update(base_step + 3, {"name": input_data['name'], "status": "image generated"})
            
            if input_data.get('generate_voice'):
                processed_content['voice_url'] = self.generate_voice_content(processed_content['audio_narration'])
                progress_tracker.update(base_step + 4, {"name": input_data['name'], "status": "voice generated"})
            
            if input_data.get('generate_music'):
                processed_content['music_url'] = self.generate_music_content(input_data)
                progress_tracker.update(base_step + 5, {"name": input_data['name'], "status": "music generated"})
            
            if input_data.get('generate_video'):
                processed_content['video_url'] = self.generate_video_content(processed_content)
                progress_tracker.update(base_step + 6, {"name": input_data['name'], "status": "video generated"})

            self.save_to_database(processed_content, input_data['name'])
            progress_tracker.update(base_step + 6, {"name": input_data['name'], "status": "completed"})
            return processed_content
        except Exception as e:
            self.logger.error(f"Error creating content for {input_data['name']}: {str(e)}", exc_info=True)
            raise

    def process_generated_content(self, generated_content: VideoContent, input_data: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'name': input_data['name'],
            'title': generated_content.video_title,
            'description': generated_content.description,
            'scenes': [scene.dict() for scene in generated_content.main_scenes],
            'audio_narration': '\n'.join([scene.scene_description for scene in generated_content.main_scenes])
        }

    def generate_image_content(self, description: str) -> str:
        try:
            return generate_image(description)
        except Exception as e:
            self.logger.error(f"Error generating image: {str(e)}", exc_info=True)
            return ""

    def generate_voice_content(self, script: str) -> str:
        try:
            return generate_voice(script)
        except Exception as e:
            self.logger.error(f"Error generating voice: {str(e)}", exc_info=True)
            return ""

    def generate_music_content(self, input_data: Dict[str, Any]) -> str:
        try:
            return generate_music(f"Create {input_data.get('style', 'background')} music for a video about {input_data['name']}")
        except Exception as e:
            self.logger.error(f"Error generating music: {str(e)}", exc_info=True)
            return ""

    def generate_video_content(self, processed_content: Dict[str, Any]) -> str:
        try:
            video_data = {
                "script": processed_content['audio_narration'],
                "image_url": processed_content.get('image_url'),
                "voice_url": processed_content.get('voice_url'),
                "music_url": processed_content.get('music_url')
            }
            return generate_video(video_data)
        except Exception as e:
            self.logger.error(f"Error generating video: {str(e)}", exc_info=True)
            return ""

    def save_to_database(self, processed_content: Dict[str, Any], name: str):
        try:
            content = Content(
                name=name,
                title=processed_content['title'],
                description=processed_content['description'],
                content=json.dumps(processed_content)
            )
            db.session.add(content)
            db.session.commit()
            self.logger.info(f"Saved content to database for {name}")
        except Exception as e:
            self.logger.error(f"Error saving to database: {str(e)}", exc_info=True)
            db.session.rollback()
            raise

    def load_input_from_csv(self, file_path: str) -> List[Dict[str, Any]]:
        input_data = []
        try:
            with open(file_path, 'r') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    input_data.append(row)
            return input_data
        except Exception as e:
            self.logger.error(f"Error loading input from CSV: {str(e)}", exc_info=True)
            raise

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Initialize the pipeline
content_pipeline = ContentCreationPipeline()

def content_creation_worker(template_name: str, run_parameters: Dict[str, Any], variable_inputs: List[Dict[str, Any]], app=None) -> List[Dict[str, Any]]:
    logger = logging.getLogger(__name__)
    logger.info(f"Starting content creation for {len(variable_inputs)} entries using template: {template_name}")
    
    try:
        input_data = [{**run_parameters, **entry, 'template': template_name} for entry in variable_inputs]
        results = content_pipeline.process_input(input_data)
        return results
    except Exception as e:
        logger.error(f"Error in content creation: {str(e)}", exc_info=True)
        return [{"error": f"Failed to generate content: {str(e)}"}]
    logger = logging.getLogger(__name__)
    logger.info(f"Starting content creation for {len(variable_inputs)} entries using template: {template_name}")
    
    try:
        input_data = [{**run_parameters, **entry, 'template': template_name} for entry in variable_inputs]
        results = content_pipeline.process_input(input_data)
        return results
    except Exception as e:
        logger.error(f"Error in content creation: {str(e)}", exc_info=True)
        return [{"error": f"Failed to generate content: {str(e)}"}]