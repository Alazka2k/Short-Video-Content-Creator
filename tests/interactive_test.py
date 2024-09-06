import os
import sys
import logging

# Add the project root directory to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.schemas import VideoContent
from src.app import create_app
from src.content_creation import ContentCreator
from src.progress_tracker import ProgressTracker
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
    load_dotenv()  # Load environment variables
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
                "imageGeneration": inputs[6].lower() == 'y',
                "voiceGeneration": inputs[7].lower() == 'y',
                "musicGeneration": inputs[8].lower() == 'y',
                "videoGeneration": inputs[9].lower() == 'y'
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

    app.logger.info(f"Input data: {input_data}")
    
    # Use app context
    with app.app_context():
        try:
            # Create a ProgressTracker instance
            progress_tracker = ProgressTracker(total_steps=5)  # Assume 5 steps for content creation

            # Generate content using the ContentCreator
            generated_content = content_creator.create_content(input_data, is_test=use_template, progress_tracker=progress_tracker)
            
            # Log the generated content
            app.logger.info(f"Generated content: {generated_content}")
            
            # Perform some assertions or checks on the generated content
            assert generated_content is not None, "Content generation failed"
            assert generated_content.generated_content, "Generated content is empty"
            
            # Parse the generated content
            video_content = VideoContent.parse_raw(generated_content.generated_content)
            
            print("\n--- Generated Content ---")
            print(f"Title: {video_content.video_title}")
            print(f"Description: {video_content.description}")
            print("\nScenes:")
            for i, scene in enumerate(video_content.main_scenes, 1):
                print(f"\nScene {i}:")
                print(f"Description: {scene.scene_description}")
                print(f"Visual Prompt: {scene.visual_prompt}")

            # Test progress tracking
            final_progress = progress_tracker.get_progress()
            print("\n--- Progress Tracking ---")
            print(f"Final progress: {final_progress['progress_percentage']}%")
            print(f"Total steps completed: {final_progress['current_step']} / {final_progress['total_steps']}")
            print(f"Total time taken: {final_progress['elapsed_time']} seconds")

            print("Content generation and progress tracking successful!")
        except Exception as e:
            app.logger.error(f"Error during content generation: {str(e)}")
            print(f"Test failed: {str(e)}")

if __name__ == "__main__":
    main()