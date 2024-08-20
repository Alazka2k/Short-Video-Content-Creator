import logging
from flask import current_app
from models import db, Content
from services import generate_content_with_openai
from typing import Dict, Any, List
import os
from dotenv import load_dotenv
import csv
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from progress_tracker import ProgressTracker

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

    def process_input(self, input_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        results = []
        total_entries = len(input_data)
        progress_tracker = ProgressTracker(total_entries)

        with ThreadPoolExecutor() as executor:
            future_to_entry = {executor.submit(self.create_content, entry, index, total_entries, progress_tracker): entry for index, entry in enumerate(input_data, start=1)}
            for future in as_completed(future_to_entry):
                entry = future_to_entry[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    logging.error(f"Error processing entry: {entry['name']} - {str(e)}")
                    results.append({"error": str(e), "name": entry['name']})

        return results

    def create_content(self, input_data: Dict[str, Any], index: int, total_entries: int, progress_tracker: ProgressTracker) -> Dict[str, Any]:
        logging.info(f"Processing entry {index}/{total_entries}: {input_data['name']}")
        template_name = input_data.get('template', 'basic')
        prompt = self.prompt_generator.generate_prompt(template_name, input_data)
        generated_content = generate_content_with_openai(prompt)
        processed_content = self.process_generated_content(generated_content, input_data)
        self.save_to_database(processed_content, input_data['name'])
        progress_tracker.update(index, {"name": input_data['name'], "status": "completed"})
        return processed_content

    def process_generated_content(self, generated_content: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
        # Parse the generated content into structured data
        content_lines = generated_content.split('\n')
        processed_content = {
            'name': input_data['name'],
            'title': content_lines[0] if content_lines else '',
            'description': content_lines[1] if len(content_lines) > 1 else '',
            'scenes': [],
            'audio_narration': ''
        }

        # Extract scenes and audio narration
        scene_start = False
        audio_start = False
        for line in content_lines[2:]:
            if line.startswith("Scene "):
                scene_start = True
                audio_start = False
                processed_content['scenes'].append(line)
            elif line.startswith("Audio Narration:"):
                scene_start = False
                audio_start = True
            elif scene_start:
                processed_content['scenes'][-1] += f"\n{line}"
            elif audio_start:
                processed_content['audio_narration'] += f"{line}\n"

        return processed_content

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
            logging.info(f"Saved content to database for {name}")
        except Exception as e:
            logging.error(f"Error saving to database: {str(e)}")
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
            logging.error(f"Error loading input from CSV: {str(e)}")
            raise

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize the pipeline
content_pipeline = ContentCreationPipeline()

def content_creation_worker(template_name: str, run_parameters: Dict[str, Any], variable_inputs: List[Dict[str, Any]], app=None) -> List[Dict[str, Any]]:
    logging.info(f"Starting content creation for {len(variable_inputs)} entries using template: {template_name}")
    
    try:
        input_data = [{**run_parameters, **entry, 'template': template_name} for entry in variable_inputs]
        results = content_pipeline.process_input(input_data)
        return results
    except Exception as e:
        logging.error(f"Error in content creation: {str(e)}")
        return [{"error": f"Failed to generate content: {str(e)}"}]