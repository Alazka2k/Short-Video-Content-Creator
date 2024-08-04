# tests/test_services.py

import unittest
from unittest.mock import patch, MagicMock
from src.services import LLMClient, MockLLMClient

class TestLLMClient(unittest.TestCase):
    @patch('src.services.Anthropic')
    def test_llm_client_initialization(self, mock_anthropic):
        client = LLMClient()
        self.assertIsNotNone(client.client)
        self.assertEqual(client.model, "claude-3-5-sonnet-20240620")

    @patch('src.services.Anthropic')
    def test_generate_content_success(self, mock_anthropic):
        mock_message = MagicMock()
        mock_message.content = [MagicMock(text="Generated content")]
        mock_anthropic.return_value.messages.create.return_value = mock_message

        client = LLMClient()
        result = client.generate_content("Test prompt")
        self.assertEqual(result, "Generated content")

    @patch('src.services.Anthropic')
    def test_generate_content_failure(self, mock_anthropic):
        mock_anthropic.return_value.messages.create.side_effect = Exception("API error")

        client = LLMClient()
        with self.assertRaises(Exception):
            client.generate_content("Test prompt")

class TestMockLLMClient(unittest.TestCase):
    def test_mock_generate_content(self):
        client = MockLLMClient()
        result = client.generate_content("Tell me about audio script")
        self.assertIn("mock audio script", result)

        result = client.generate_content("Describe a scene")
        self.assertIn("Imagine a scene", result)

        result = client.generate_content("Generic prompt")
        self.assertIn("generic mock response", result)

if __name__ == '__main__':
    unittest.main()