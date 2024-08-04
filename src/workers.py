# src/workers.py

from src.prompt_generator import PromptGenerator
from src.services import llm_client
from src.models import db, Content
import logging

prompt_generator = PromptGenerator('src/prompt_templates.yaml')

def content_creation_worker(initial_prompt, run_parameters, variable_inputs):
    logging.info(f"Starting content creation for {variable_inputs['name']}")
    
    try:
        # Generate the full prompt using the PromptGenerator
        full_prompt = prompt_generator.generate_prompt('video_content', {
            'name': variable_inputs['name'],
            'scene_amount': run_parameters['scene_amount'],
            'video_length': run_parameters['video_length'],
            'image_style': run_parameters['image_style']
        })
        
        # Validate the generated prompt
        if not prompt_generator.validate_prompt(full_prompt):
            raise ValueError("Generated prompt is invalid")
        
        # Generate content using the LLM
        generated_content = llm_client.generate_content(full_prompt)
        
        if not generated_content:
            raise ValueError("Generated content is empty")
        
        # Process the generated content
        processed_content = process_generated_content(generated_content)
        
        # Generate audio scripts for each scene
        processed_content = generate_audio_scripts(processed_content, variable_inputs['name'])
        
        # Save to database
        save_to_database(processed_content, variable_inputs['name'])
        
        return processed_content
    except Exception as e:
        logging.error(f"Error in content creation: {str(e)}")
        return {"error": f"Failed to generate content: {str(e)}"}

def process_generated_content(generated_content):
    lines = generated_content.strip().split('\n')
    processed_content = {
        'title': '',
        'description': '',
        'scenes': []
    }

    current_section = None
    for line in lines:
        line = line.strip()
        if line.startswith('1. Video Title:'):
            processed_content['title'] = line.split(':', 1)[1].strip()
        elif line.startswith('2. Description:'):
            processed_content['description'] = line.split(':', 1)[1].strip()
        elif line.startswith('3. Main Scenes:'):
            current_section = 'scenes'
        elif current_section == 'scenes' and line.startswith('-'):
            scene_type, scene_content = line.split(':', 1)
            if 'Scene description' in scene_type:
                processed_content['scenes'].append({'description': scene_content.strip(), 'visual_prompt': ''})
            elif 'Visual prompt' in scene_type and processed_content['scenes']:
                processed_content['scenes'][-1]['visual_prompt'] = scene_content.strip()

    return processed_content

def generate_audio_scripts(processed_content, name):
    for i, scene in enumerate(processed_content['scenes']):
        audio_prompt = prompt_generator.generate_prompt('scene_audio_script', {
            'name': name,
            'scene_description': scene['description'],
            'audio_length': 15,  # Assume 15 seconds per scene, adjust as needed
            'tone': 'Informative',
            'audience': 'General public'
        })
        
        # Generate audio script using the LLM
        audio_script = llm_client.generate_content(audio_prompt)
        
        # Add the audio script to the scene
        scene['audio_script'] = audio_script

    return processed_content

def save_to_database(processed_content, name):
    content = Content(
        name=name,
        title=processed_content['title'],
        description=processed_content['description'],
        content=str(processed_content)
    )
    db.session.add(content)
    db.session.commit()