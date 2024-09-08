# backend/unit_tests/test_services.py   

import pytest
from unittest.mock import patch, MagicMock
from backend.src import VideoScript, Scene, generate_content_with_openai, load_config


@pytest.fixture
def mock_config():
    return {'openai': {'model': 'test-model'}}

class TestServices:
    @patch('backend.src.services.client.chat.completions.create')
    @patch('backend.src.services.load_config')
    def test_generate_content_with_openai(self, mock_load_config, mock_create, mock_config):
        mock_load_config.return_value = mock_config
        mock_response = MagicMock()
        mock_response.choices[0].message.content = json.dumps({
            "title": "Test Title",
            "description": "Test Description",
            "scenes": [
                {
                    "description": "Scene 1",
                    "visual_prompt": "Visual 1"
                },
                {
                    "description": "Scene 2",
                    "visual_prompt": "Visual 2"
                }
            ]
        })
        mock_create.return_value = mock_response

        result = generate_content_with_openai("Test prompt")
        assert isinstance(result, VideoScript)
        assert result.title == "Test Title"
        assert result.description == "Test Description"
        assert len(result.scenes) == 2
        assert result.scenes[0].description == "Scene 1"
        assert result.scenes[1].visual_prompt == "Visual 2"

        mock_create.assert_called_once_with(
            model='test-model',
            messages=[
                {"role": "system", "content": "You are a creative video content creator. Generate a video concept based on the user's prompt. Your response should be a JSON object with the following structure: {title: string, description: string, scenes: [{description: string, visual_prompt: string}]}"},
                {"role": "user", "content": "Test prompt"}
            ],
            response_format={"type": "json_object"}
        )

    @patch('backend.src.services.client.chat.completions.create')
    @patch('backend.src.services.load_config')
    def test_generate_content_with_openai_error(self, mock_load_config, mock_create, mock_config):
        mock_load_config.return_value = mock_config
        mock_create.side_effect = Exception("API Error")
        
        with pytest.raises(Exception, match="Error in content generation: API Error"):
            generate_content_with_openai("Test prompt")

# Andere Tests bleiben unverändert