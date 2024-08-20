import unittest
from unittest.mock import patch, MagicMock
from services import OpenAIService, generate_content_with_openai
import json

class TestOpenAIService(unittest.TestCase):

    def setUp(self):
        self.service = OpenAIService()

    @patch('services.client.chat.completions.create')
    def test_generate_content_success(self, mock_create):
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '{"title": "Test", "description": "This is a test"}'
        mock_create.return_value = mock_response

        result = self.service.generate_content("Test prompt")
        
        self.assertEqual(result, {"title": "Test", "description": "This is a test"})
        mock_create.assert_called_once()

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
        mock_generate.return_value = {"title": "Test"}
        
        result = generate_content_with_openai("Test prompt")
        
        self.assertEqual(result, {"title": "Test"})
        mock_generate.assert_called_once_with("Test prompt")

if __name__ == '__main__':
    unittest.main()