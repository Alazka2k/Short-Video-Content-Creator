import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(current_dir), 'src')
sys.path.insert(0, src_dir)

from workers import PromptGenerator, content_creation_worker

class TestWorkers(unittest.TestCase):
    def setUp(self):
        self.prompt_generator = PromptGenerator()

    def test_generate_prompt(self):
        prompt = self.prompt_generator.generate_prompt("basic", {"name": "Test Name", "scene_amount": 5})
        self.assertIn("Test Name", prompt)
        self.assertIn("5 scenes", prompt)

    @patch('workers.generate_content_with_openai')
    @patch('workers.process_generated_content')
    @patch('workers.save_to_database')
    def test_content_creation_worker(self, mock_save, mock_process, mock_generate):
        mock_generate.return_value = "Generated content"
        mock_process.return_value = {"title": "Test Title", "description": "Test Description"}

        result = content_creation_worker("basic", {"scene_amount": 5}, {"name": "Test Name"})

        self.assertEqual(result, {"title": "Test Title", "description": "Test Description"})
        mock_generate.assert_called_once()
        mock_process.assert_called_once_with("Generated content", {"scene_amount": 5})
        mock_save.assert_called_once()

if __name__ == '__main__':
    unittest.main()