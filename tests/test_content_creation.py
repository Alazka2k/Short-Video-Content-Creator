# tests/test_content_creation.py

import unittest
from unittest.mock import patch, MagicMock
from src.workers import content_creation_worker, process_generated_content, generate_audio_scripts

class TestContentCreation(unittest.TestCase):
    @patch('src.workers.llm_client')
    @patch('src.workers.save_to_database')
    def test_content_creation_worker(self, mock_save_to_database, mock_llm_client):
        mock_llm_client.generate_content.return_value = """
        1. Video Title: The Incredible Life of Albert Einstein
        2. Description: Journey through the extraordinary life of Albert Einstein, from his curiosity-filled childhood to his world-changing scientific discoveries.
        3. Main Scenes:
        - Scene description: Young Einstein fascinated by a compass
        - Visual prompt: Close-up of a young boy's hands holding a compass, with a look of wonder on his face
        - Scene description: Einstein working as a patent clerk
        - Visual prompt: Einstein at a desk surrounded by papers and inventions, looking deep in thought
        - Scene description: Einstein presenting his theory of relativity
        - Visual prompt: Einstein writing E=mc² on a chalkboard in front of a captivated audience
        """

        initial_prompt = "Create a video about a famous scientist"
        run_parameters = {"scene_amount": 3, "video_length": 60, "image_style": "Realistic"}
        variable_inputs = {"name": "Albert Einstein"}

        result = content_creation_worker(initial_prompt, run_parameters, variable_inputs)

        self.assertEqual(result['title'], "The Incredible Life of Albert Einstein")
        self.assertIn("Journey through the extraordinary life", result['description'])
        self.assertEqual(len(result['scenes']), 3)
        self.assertIn("audio_script", result['scenes'][0])

    def test_process_generated_content(self):
        generated_content = """
        1. Video Title: The Incredible Life of Albert Einstein
        2. Description: Journey through the extraordinary life of Albert Einstein, from his curiosity-filled childhood to his world-changing scientific discoveries.
        3. Main Scenes:
        - Scene description: Young Einstein fascinated by a compass
        - Visual prompt: Close-up of a young boy's hands holding a compass, with a look of wonder on his face
        - Scene description: Einstein working as a patent clerk
        - Visual prompt: Einstein at a desk surrounded by papers and inventions, looking deep in thought
        """

        result = process_generated_content(generated_content)

        self.assertEqual(result['title'], "The Incredible Life of Albert Einstein")
        self.assertIn("Journey through the extraordinary life", result['description'])
        self.assertEqual(len(result['scenes']), 2)
        self.assertEqual(result['scenes'][0]['description'], "Young Einstein fascinated by a compass")
        self.assertEqual(result['scenes'][0]['visual_prompt'], "Close-up of a young boy's hands holding a compass, with a look of wonder on his face")

    @patch('src.workers.llm_client')
    def test_generate_audio_scripts(self, mock_llm_client):
        mock_llm_client.generate_content.return_value = "This is a mock audio script."

        processed_content = {
            'scenes': [
                {'description': 'Scene 1 description'},
                {'description': 'Scene 2 description'}
            ]
        }

        result = generate_audio_scripts(processed_content, "Albert Einstein")

        self.assertEqual(len(result['scenes']), 2)
        self.assertEqual(result['scenes'][0]['audio_script'], "This is a mock audio script.")
        self.assertEqual(result['scenes'][1]['audio_script'], "This is a mock audio script.")

if __name__ == '__main__':
    unittest.main()