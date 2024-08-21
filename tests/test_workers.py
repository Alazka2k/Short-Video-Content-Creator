import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(current_dir), 'src')
sys.path.insert(0, src_dir)

from workers import PromptGenerator, content_creation_worker, ContentCreationPipeline

class TestWorkers(unittest.TestCase):
    def setUp(self):
        self.prompt_generator = PromptGenerator()

    def test_generate_prompt(self):
        prompt = self.prompt_generator.generate_prompt("basic", {"name": "Test Name", "scene_amount": 5})
        self.assertIn("Test Name", prompt)
        self.assertIn("5 scenes", prompt)

    @patch('workers.generate_content_with_openai')
    @patch('workers.generate_image')
    @patch('workers.generate_voice')
    @patch('workers.generate_music')
    @patch('workers.generate_video')
    def test_content_creation_worker(self, mock_video, mock_music, mock_voice, mock_image, mock_openai):
        mock_openai.return_value = {
            "title": "Generated Title",
            "description": "Generated Description",
            "scenes": ["Scene 1", "Scene 2"],
            "audio_narration": "Generated Audio"
        }
        mock_image.return_value = "http://example.com/image.jpg"
        mock_voice.return_value = "http://example.com/voice.mp3"
        mock_music.return_value = "http://example.com/music.mp3"
        mock_video.return_value = "http://example.com/video.mp4"

        result = content_creation_worker("basic", 
                                         {"scene_amount": 5}, 
                                         [{"name": "Test Name", 
                                           "generate_image": True, 
                                           "generate_voice": True, 
                                           "generate_music": True, 
                                           "generate_video": True}])

        self.assertEqual(len(result), 1)
        content = result[0]
        self.assertEqual(content["title"], "Generated Title")
        self.assertEqual(content["description"], "Generated Description")
        self.assertEqual(content["image_url"], "http://example.com/image.jpg")
        self.assertEqual(content["voice_url"], "http://example.com/voice.mp3")
        self.assertEqual(content["music_url"], "http://example.com/music.mp3")
        self.assertEqual(content["video_url"], "http://example.com/video.mp4")

    @patch('workers.generate_content_with_openai')
    @patch('workers.generate_image')
    @patch('workers.generate_voice')
    @patch('workers.generate_music')
    @patch('workers.generate_video')
    def test_content_creation_pipeline(self, mock_video, mock_music, mock_voice, mock_image, mock_openai):
        mock_openai.return_value = {
            "title": "Generated Title",
            "description": "Generated Description",
            "scenes": ["Scene 1", "Scene 2"],
            "audio_narration": "Generated Audio"
        }
        mock_image.return_value = "http://example.com/image.jpg"
        mock_voice.return_value = "http://example.com/voice.mp3"
        mock_music.return_value = "http://example.com/music.mp3"
        mock_video.return_value = "http://example.com/video.mp4"

        pipeline = ContentCreationPipeline()
        input_data = {
            "name": "Test Name",
            "template": "basic",
            "scene_amount": 5,
            "generate_image": True,
            "generate_voice": True,
            "generate_music": True,
            "generate_video": True
        }

        with patch.object(pipeline, 'save_to_database'):
            result = pipeline.create_content(input_data, 1, 1, MagicMock())

        self.assertEqual(result["name"], "Test Name")
        self.assertEqual(result["title"], "Generated Title")
        self.assertEqual(result["description"], "Generated Description")
        self.assertEqual(result["image_url"], "http://example.com/image.jpg")
        self.assertEqual(result["voice_url"], "http://example.com/voice.mp3")
        self.assertEqual(result["music_url"], "http://example.com/music.mp3")
        self.assertEqual(result["video_url"], "http://example.com/video.mp4")

    def test_process_generated_content(self):
        pipeline = ContentCreationPipeline()
        generated_content = {
            "raw_content": "Title\nDescription\nScene 1\nScene 2\nAudio Narration:\nNarration text"
        }
        input_data = {"name": "Test Name"}

        result = pipeline.process_generated_content(generated_content, input_data)

        self.assertEqual(result["name"], "Test Name")
        self.assertEqual(result["title"], "Title")
        self.assertEqual(result["description"], "Description")
        self.assertEqual(result["scenes"], ["Scene 1", "Scene 2"])
        self.assertEqual(result["audio_narration"], "Narration text\n")

if __name__ == '__main__':
    unittest.main()