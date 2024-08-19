# User Guide

This guide provides instructions on how to use the Short Video Content Creator.

## Getting Started

1. Ensure you've completed the installation process as described in the Installation Guide.

2. Start the Flask server:
   ```
   python src/server.py
   ```

3. The server will start running on `http://localhost:5000`.

## Creating a Video

1. Prepare your input data:
   - Decide on the subject of your video (e.g., a notable scientist or inventor)
   - Gather key information about the subject

2. Make a POST request to the `/create_content` endpoint:
   ```
   POST http://localhost:5000/create_content
   Content-Type: application/json

   {
     "template_name": "video_content",
     "run_parameters": {
       "scene_amount": 5,
       "video_length": 60
     },
     "variable_inputs": {
       "name": "Albert Einstein",
       "image_style": "Cinematic"
     }
   }
   ```

3. The server will process your request and return a JSON response with the generated content.

4. Use the returned content to guide your video creation process.

## Using the Prompt Generation System

1. Import the PromptGenerator:
   ```python
   from src.prompt_generator import PromptGenerator
   ```

2. Initialize the PromptGenerator with your template file:
   ```python
   generator = PromptGenerator('src/prompt_templates.yaml')
   ```

3. Generate a prompt:
   ```python
   variables = {
       'name': 'Marie Curie',
       'scene_amount': 5,
       'video_length': 60,
       'image_style': 'Documentary'
   }
   prompt = generator.generate_prompt('video_content', variables)
   ```

4. Use the generated prompt in your content creation process.

For more detailed examples, refer to `examples/prompt_generator_examples.py`.

## Customizing Templates

You can add or modify prompt templates in the `src/prompt_templates.yaml` file. Each template should have a name, a template string, and an optional maximum length.

## Troubleshooting

If you encounter any issues while using the Short Video Content Creator, please check the following:

- Ensure the Flask server is running
- Check that your API keys in the `.env` file are correct and not expired
- Verify that your input data is correctly formatted

If problems persist, please open an issue on the GitHub repository.