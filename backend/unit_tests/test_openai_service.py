import unittest
from unittest.mock import patch, MagicMock
from src.services import OpenAIService, generate_content_with_openai
import json
import os
from dotenv import load_dotenv
from backend.src.models import VideoContent

# Laden Sie die .env-Datei aus dem Hauptverzeichnis
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

class TestOpenAIService(unittest.TestCase):

    def setUp(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY nicht in der .env-Datei gefunden")
        self.service = OpenAIService(api_key)

    @patch('services.client.chat.completions.create')
    def test_generate_content_success(self, mock_create):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = json.dumps({
            "video_title": "Test Title",
            "description": "Test Description",
            "main_scenes": [
                {"scene_description": "Scene 1", "visual_prompt": "Visual 1"}
            ]
        })
        mock_create.return_value = mock_response

        result = self.service.generate_content("Test prompt")
        self.assertIsInstance(result, dict)
        self.assertEqual(result["video_title"], "Test Title")

    @patch('services.client.chat.completions.create')
    def test_generate_content_non_json(self, mock_create):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = 'This is not JSON'
        mock_create.return_value = mock_response

        result = self.service.generate_content("Test prompt")
        
        self.assertEqual(result, {"raw_content": "This is not JSON"})

    @patch('services.client.chat.completions.create')
    def test_generate_content_api_error(self, mock_create):
        mock_create.side_effect = Exception("API Error")

        with self.assertRaises(Exception):
            self.service.generate_content("Test prompt")

    @patch('services.openai_service.generate_content')
    def test_generate_content_with_openai(self, mock_generate):
        mock_generate.return_value = VideoContent(
            video_title="Test Title",
            description="Test Description",
            main_scenes=[{"scene_description": "Scene 1", "visual_prompt": "Visual 1"}]
        )

        result = generate_content_with_openai("Test prompt")
        self.assertIsInstance(result, VideoContent)

if __name__ == '__main__':
    unittest.main()