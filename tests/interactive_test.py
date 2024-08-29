import os
import sys
import logging

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.schemas import VideoContent
from src.app import create_app
from src.content_creation import ContentCreator
from dotenv import load_dotenv


def read_input_file():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file_path = os.path.join(current_dir, 'test_input.txt')
    
    with open(input_file_path, 'r') as file:
        lines = file.readlines()
    
    return [line.strip() for line in lines]

def get_manual_input():
    inputs = []
    prompts = [
        "Enter the title of the video: ",
        "Enter a brief description: ",
        "Enter the target audience: ",
        "Enter the duration in seconds: ",
        "Enter the style (e.g., informative, entertaining): ",
        "Enter the number of scenes: ",
        "Generate images? (y/n): ",
        "Generate voice? (y/n): ",
        "Generate music? (y/n): ",
        "Generate video? (y/n): "
    ]
    for prompt in prompts:
        inputs.append(input(prompt))
    return inputs

def main():
    app = create_app()
    template_file_path = os.path.join(project_root, "src", "prompt_templates.yaml")
    test_input_path = os.path.join(project_root, "tests", "test_input.txt")
    content_creator = ContentCreator(template_file_path, test_input_path)

    use_template = input("Use template input? (y/n): ").lower() == 'y'
    
    if use_template:
        inputs = read_input_file()
        input_data = {
            "title": f"A video about {inputs[0]}",
            "description": inputs[1],
            "target_audience": inputs[2],
            "duration": int(inputs[3]),
            "style": inputs[4],
            "scene_amount": int(inputs[5]),
            "video_length": int(inputs[3]),
            "image_style": inputs[4],
            "services": {
                "contentGeneration": True,
                "imageGeneration": False,
                "voiceGeneration": False,
                "musicGeneration": False,
                "videoGeneration": False
            }
        }
    else:
        inputs = get_manual_input()
        input_data = {
            "title": inputs[0],
            "description": inputs[1],
            "target_audience": inputs[2],
            "duration": int(inputs[3]),
            "style": inputs[4],
            "scene_amount": int(inputs[5]),
            "video_length": int(inputs[3]),  # Assuming duration and video_length are the same
            "image_style": "realistic",  # Add this line or get it from user input
            "services": {
                "contentGeneration": True,
                "imageGeneration": inputs[6].lower() == 'y',
                "voiceGeneration": inputs[7].lower() == 'y',
                "musicGeneration": inputs[8].lower() == 'y',
                "videoGeneration": inputs[9].lower() == 'y'
            }
        }

    # Remove 'name' from input_data if it exists
    input_data.pop('name', None)

    app.logger.info(f"Input data: {input_data}")
    
    # Use app context
    with app.app_context():
        try:
            # Generate content using the ContentCreator
            generated_content = content_creator.create_content(input_data, is_test=use_template)
            
            # Log the generated content
            app.logger.info(f"Generated content: {generated_content}")
            
            # Perform some assertions or checks on the generated content
            assert generated_content is not None, "Content generation failed"
            assert len(generated_content) > 0, "Generated content is empty"
            
            # Detailed checks for scenes and image prompts
            assert 'scenes' in generated_content, "Scenes not found in generated content"
            assert len(generated_content['scenes']) == input_data['scene_amount'], f"Expected {input_data['scene_amount']} scenes, but got {len(generated_content['scenes'])}"

            print("\n--- Scene Details ---")
            for i, scene in enumerate(generated_content['scenes'], 1):
                print(f"\nScene {i}:")
                print(f"Description: {scene.get('description', 'N/A')}")
                print(f"Duration: {scene.get('duration', 'N/A')} seconds")
                print(f"Script: {scene.get('script', 'N/A')}")

            if input_data['services']['imageGeneration']:
                assert 'image_prompts' in generated_content, "Image prompts not found when image generation was requested"
                assert len(generated_content['image_prompts']) > 0, "No image prompts generated"

                print("\n--- Image Prompts ---")
                for i, prompt in enumerate(generated_content['image_prompts'], 1):
                    print(f"\nImage {i}:")
                    print(f"Prompt: {prompt}")

            print("All specific content checks passed!")
        except Exception as e:
            app.logger.error(f"Error during content generation: {str(e)}")
            print(f"Test failed: {str(e)}")

if __name__ == "__main__":
    main()