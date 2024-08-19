# tests/test_prompt_generator.py

import unittest
import os
from src.prompt_generator import PromptGenerator

class TestPromptGenerator(unittest.TestCase):
    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(current_dir, '..', 'src', 'prompt_templates.yaml')
        self.prompt_generator = PromptGenerator(template_path)

    def test_load_templates(self):
        self.assertIn('video_content', self.prompt_generator.templates)
        self.assertIn('scene_audio_script', self.prompt_generator.templates)
        self.assertIn('image_generation', self.prompt_generator.templates)

    def test_generate_prompt(self):
        variables = {
            'name': 'Albert Einstein',
            'scene_amount': 5,
            'video_length': 60,
            'image_style': 'Cinematic'
        }
        prompt = self.prompt_generator.generate_prompt('video_content', variables)
        self.assertIn('Albert Einstein', prompt)
        self.assertIn('5 scenes', prompt)
        self.assertIn('60 seconds', prompt)
        self.assertIn('Cinematic', prompt)

    def test_validate_prompt(self):
        valid_prompt = "This is a valid prompt."
        self.assertTrue(self.prompt_generator.validate_prompt(valid_prompt, 'video_content'))

        empty_prompt = ""
        self.assertFalse(self.prompt_generator.validate_prompt(empty_prompt, 'video_content'))

        prompt_with_placeholders = "This prompt has an unfilled {placeholder}."
        self.assertFalse(self.prompt_generator.validate_prompt(prompt_with_placeholders, 'video_content'))

    def test_get_required_variables(self):
        variables = self.prompt_generator.get_required_variables('video_content')
        self.assertIn('name', variables)
        self.assertIn('scene_amount', variables)
        self.assertIn('video_length', variables)
        self.assertIn('image_style', variables)

    def test_add_and_remove_template(self):
        self.prompt_generator.add_template('test_template', 'This is a test template for $name.')
        self.assertIn('test_template', self.prompt_generator.templates)

        self.prompt_generator.remove_template('test_template')
        self.assertNotIn('test_template', self.prompt_generator.templates)

    def test_component_expansion(self):
        self.prompt_generator.components['test_component'] = "This is a test component."
        self.prompt_generator.add_template('component_test', '{component:test_component} $name')
        
        prompt = self.prompt_generator.generate_prompt('component_test', {'name': 'John'})
        self.assertEqual(prompt, "This is a test component. John")

if __name__ == '__main__':
    unittest.main()