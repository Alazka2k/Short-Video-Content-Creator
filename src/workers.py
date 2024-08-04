import logging
from flask import current_app
from models import db, Content
from services import llm_client

def content_creation_worker(initial_prompt, run_parameters, variable_inputs):
    logging.info(f"Starting content creation for {variable_inputs['name']}")
    
    try:
        # Construct the full prompt
        full_prompt = construct_full_prompt(initial_prompt, run_parameters, variable_inputs)
        
        # Generate content using the LLM
        generated_content = llm_client.generate_content(full_prompt)
        
        # Process the generated content
        processed_content = process_generated_content(generated_content, run_parameters)
        
        # Save to database
        save_to_database(processed_content, variable_inputs['name'])
        
        return processed_content
    except Exception as e:
        logging.error(f"Error in content creation: {str(e)}")
        return {"error": f"Failed to generate content: {str(e)}"}

def construct_full_prompt(initial_prompt, run_parameters, variable_inputs):
    # Combine the initial prompt, run parameters, and variable inputs into a single prompt
    full_prompt = initial_prompt.format(
        name=variable_inputs['name'],
        scene_amount=run_parameters['scene_amount'],
        **run_parameters
    )
    logging.info(f"Constructed full prompt: {full_prompt[:100]}...")  # Log first 100 chars
    return full_prompt

def process_generated_content(generated_content, run_parameters):
    # Process the LLM's output based on run parameters
    # This is a placeholder implementation. Adjust according to your specific needs.
    scenes = generated_content.split('\n')
    processed_content = {
        'title': scenes[0],
        'description': scenes[1],
        'hashtags': scenes[2],
        'opening_scene': scenes[3],
        'main_scenes': scenes[4:-1],
        'closing_scene': scenes[-1]
    }
    logging.info(f"Processed content: {processed_content}")
    return processed_content

def save_to_database(processed_content, name):
    # Save the processed content to the database
    with current_app.app_context():
        content = Content(
            name=name,
            title=processed_content['title'],
            description=processed_content['description'],
            content=str(processed_content)  # Convert dict to string for storage
        )
        db.session.add(content)
        db.session.commit()
    logging.info(f"Saved content to database for {name}")