# tests/test_prompt_generator.py

import unittest
from src.prompt_generator import PromptGenerator
import logging
from io import StringIO

class TestPromptGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = PromptGenerator('src/prompt_templates.yaml')
        self.log_capture = StringIO()
        self.log_handler = logging.StreamHandler(self.log_capture)
        logging.getLogger().addHandler(self.log_handler)
        logging.getLogger().setLevel(logging.INFO)

    def tearDown(self):
        logging.getLogger().removeHandler(self.log_handler)

    def test_load_templates(self):
        self.assertIn('video_content', self.generator.templates)
        self.assertIn('scene_audio_script', self.generator.templates)

    def test_generate_video_content_prompt(self):
        variables = {
            'name': 'Albert Einstein',
            'scene_amount': 3,
            'video_length': 60,
            'image_style': 'Realistic'
        }
        prompt = self.generator.generate_prompt('video_content', variables)
        self.assertIn('Albert Einstein', prompt)
        self.assertIn('3', prompt)
        self.assertIn('60 seconds', prompt)
        self.assertIn('Realistic', prompt)

    def test_generate_scene_audio_script_prompt(self):
        variables = {
            'name': 'Marie Curie',
            'scene_description': 'Marie Curie working in her laboratory',
            'audio_length': 15,
            'tone': 'Informative',
            'audience': 'General public'
        }
        prompt = self.generator.generate_prompt('scene_audio_script', variables)
        self.assertIn('Marie Curie', prompt)
        self.assertIn('Marie Curie working in her laboratory', prompt)
        self.assertIn('15 seconds', prompt)
        self.assertIn('Informative', prompt)
        self.assertIn('General public', prompt)

    def test_missing_template(self):
        with self.assertRaises(ValueError):
            self.generator.generate_prompt('non_existent_template', {})

    def test_missing_variable(self):
        with self.assertRaises(KeyError):
            self.generator.generate_prompt('video_content', {'name': 'Test'})
        self.assertIn("Missing variable in template: 'scene_amount'", self.log_capture.getvalue())

    def test_validate_prompt(self):
        self.assertTrue(self.generator.validate_prompt("This is a valid prompt"))
        self.assertFalse(self.generator.validate_prompt(""))
        self.assertFalse(self.generator.validate_prompt("   "))
        log_output = self.log_capture.getvalue()
        self.assertIn("Generated prompt is empty", log_output)
        self.assertEqual(log_output.count("Generated prompt is empty"), 2)

if __name__ == '__main__':
    unittest.main()