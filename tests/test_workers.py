# tests/test_workers.py

import unittest
from unittest.mock import patch, MagicMock
from src.workers import content_creation_worker

class TestContentCreationWorker(unittest.TestCase):
    @patch('src.workers.llm_client')
    @patch('src.workers.save_to_database')
    def test_content_creation_worker_success(self, mock_save_to_database, mock_llm_client):
        # Mock successful LLM response
        mock_llm_client.generate_content.return_value = """
        1. Video Title: The Extraordinary Life of Albert Einstein
        2. Description: Dive into the fascinating journey of the world's most famous physicist.
        3. Hashtags: #AlbertEinstein, #ScienceGenius, #Relativity
        4. Opening Scene: A young Albert gazes at a compass, sparking his curiosity.
        5. Main Scenes:
           1. Einstein as a patent clerk, scribbling equations.
           2. The publication of his groundbreaking papers in 1905.
           3. Einstein receiving the Nobel Prize in Physics.
        6. Closing Scene: Einstein's impact on modern physics and pop culture.
        7. Visual Prompts:
           - Opening: Close-up of a child's hand holding a compass, soft lighting.
           - Scene 1: Cluttered desk with papers, dim office lighting.
           - Scene 2: Montage of scientific journals with Einstein's papers.
           - Scene 3: Grand hall with Einstein receiving the Nobel Prize.
           - Closing: Split screen of atomic structure and Einstein merchandise.
        """

        initial_prompt = "Create a video script"
        run_parameters = {"scene_amount": 3, "video_length": 60, "image_style": "Realistic"}
        variable_inputs = {"name": "Albert Einstein"}

        result = content_creation_worker(initial_prompt, run_parameters, variable_inputs)

        self.assertEqual(result['title'], "The Extraordinary Life of Albert Einstein")
        self.assertIn("fascinating journey", result['description'])
        self.assertIn("#AlbertEinstein", result['hashtags'])
        self.assertIn("young Albert gazes at a compass", result['opening_scene'])
        self.assertEqual(len(result['main_scenes']), 3)
        self.assertIn("impact on modern physics", result['closing_scene'])

    @patch('src.workers.llm_client')
    def test_content_creation_worker_failure(self, mock_llm_client):
        # Mock LLM failure
        mock_llm_client.generate_content.return_value = None

        initial_prompt = "Create a video script"
        run_parameters = {"scene_amount": 3, "video_length": 60, "image_style": "Realistic"}
        variable_inputs = {"name": "Albert Einstein"}

        result = content_creation_worker(initial_prompt, run_parameters, variable_inputs)

        self.assertIn("error", result)
        self.assertIn("Failed to generate content", result["error"])

    @patch('src.workers.llm_client')
    def test_content_creation_worker_empty_response(self, mock_llm_client):
        # Mock LLM empty response
        mock_llm_client.generate_content.return_value = ""

        initial_prompt = "Create a video script"
        run_parameters = {"scene_amount": 3, "video_length": 60, "image_style": "Realistic"}
        variable_inputs = {"name": "Albert Einstein"}

        result = content_creation_worker(initial_prompt, run_parameters, variable_inputs)

        self.assertIn("error", result)
        self.assertIn("Failed to generate content", result["error"])

if __name__ == '__main__':
    unittest.main()