# examples/prompt_generator_examples.py

from prompt_generator import PromptGenerator

def main():
    # Initialize the PromptGenerator
    generator = PromptGenerator('../src/prompt_templates.yaml')

    # Example 1: Generating a video content prompt
    print("Example 1: Generating a video content prompt")
    video_variables = {
        'name': 'Albert Einstein',
        'scene_amount': 5,
        'video_length': 60,
        'image_style': 'Cinematic'
    }
    video_prompt = generator.generate_prompt('video_content', video_variables)
    print(video_prompt)
    print(f"Is valid: {generator.validate_prompt(video_prompt, 'video_content')}\n")

    # Example 2: Generating an audio script prompt
    print("Example 2: Generating an audio script prompt")
    audio_variables = {
        'name': 'Marie Curie',
        'scene_description': 'Marie Curie working in her laboratory',
        'audio_length': 30,
        'tone': 'informative',
        'audience': 'high school students'
    }
    audio_prompt = generator.generate_prompt('scene_audio_script', audio_variables)
    print(audio_prompt)
    print(f"Is valid: {generator.validate_prompt(audio_prompt, 'scene_audio_script')}\n")

    # Example 3: Adding a new template
    print("Example 3: Adding a new template")
    generator.add_template('custom_template', 'This is a custom template for $name about $topic.')
    custom_variables = {
        'name': 'Isaac Newton',
        'topic': 'gravity'
    }
    custom_prompt = generator.generate_prompt('custom_template', custom_variables)
    print(custom_prompt)
    print(f"Is valid: {generator.validate_prompt(custom_prompt, 'custom_template')}\n")

    # Example 4: Demonstrating validation failure
    print("Example 4: Demonstrating validation failure")
    invalid_prompt = generator.generate_prompt('video_content', {'name': 'Invalid Example'})
    print(f"Is valid: {generator.validate_prompt(invalid_prompt, 'video_content')}")

if __name__ == "__main__":
    main()