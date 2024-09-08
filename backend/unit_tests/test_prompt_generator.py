# backend/unit_tests/test_prompt_generator.py

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
        self.assertIn('image_generation', self.prompt_generator.templates)
        self.assertIn('music_generation', self.prompt_generator.templates)

    def test_generate_prompt(self):
        variables = {
            'videoSubject': 'Albert Einstein',
            'generalOptions': {
                'style': 'Documentary',
                'description': 'A video about the life of Albert Einstein',
                'sceneAmount': 5,
                'duration': 60,
                'tone': 'Informative',
                'vocabulary': 'Academic',
                'targetAudience': 'Science enthusiasts'
            },
            'contentOptions': {
                'pacing': 'Moderate',
                'description': 'Chronological overview of Einstein\'s life'
            },
            'visualPromptOptions': {
                'pictureDescription': 'Portrait of Einstein at his desk',
                'style': 'Realistic',
                'imageDetails': 'Show equations on a chalkboard',
                'shotDetails': 'Medium shot'
            }
        }
        prompt = self.prompt_generator.generate_prompt('video_content', variables)
        self.assertIn('Albert Einstein', prompt)
        self.assertIn('Documentary', prompt)
        self.assertIn('5', prompt)
        self.assertIn('60 seconds', prompt)
        self.assertIn('Science enthusiasts', prompt)

    def test_validate_prompt(self):
        valid_prompt = "This is a valid prompt."
        self.assertTrue(self.prompt_generator.validate_prompt(valid_prompt, 'video_content'))

        empty_prompt = ""
        self.assertFalse(self.prompt_generator.validate_prompt(empty_prompt, 'video_content'))

        prompt_with_placeholders = "This prompt has an unfilled {placeholder}."
        self.assertFalse(self.prompt_generator.validate_prompt(prompt_with_placeholders, 'video_content'))

    def test_get_required_variables(self):
        variables = self.prompt_generator.get_required_variables('video_content')
        self.assertIn('videoSubject', variables)
        self.assertIn('generalOptions_style', variables)
        self.assertIn('contentOptions_pacing', variables)
        self.assertIn('visualPromptOptions_pictureDescription', variables)

    def test_add_and_remove_template(self):
        self.prompt_generator.add_template('test_template', 'This is a test template for {name}.')
        self.assertIn('test_template', self.prompt_generator.templates)

        self.prompt_generator.remove_template('test_template')
        self.assertNotIn('test_template', self.prompt_generator.templates)

    def test_component_expansion(self):
        self.prompt_generator.components['test_component'] = "This is a test component."
        self.prompt_generator.add_template('component_test', '{component:test_component} {name}')
        
        prompt = self.prompt_generator.generate_prompt('component_test', {'name': 'John'})
        self.assertEqual(prompt, "This is a test component. John")

if __name__ == '__main__':
    unittest.main()