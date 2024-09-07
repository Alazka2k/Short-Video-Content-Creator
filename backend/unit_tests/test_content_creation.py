import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(current_dir), 'src')
sys.path.insert(0, src_dir)

from src.workers import content_creation_worker
from src.app import create_app, db
from src.services import VideoContent, Scene

class TestContentCreation(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch('src.workers.generate_content_with_openai')
    @patch('src.workers.generate_image')
    @patch('src.workers.generate_voice')
    @patch('src.workers.generate_music')
    @patch('src.workers.generate_video')
    def test_content_creation(self, mock_generate_video, mock_generate_music, 
                              mock_generate_voice, mock_generate_image, 
                              mock_generate_content):
        # Mock the OpenAI response
        mock_generate_content.return_value = VideoContent(
            video_title="The Life of Test Subject",
            description="A fascinating video about Test Subject",
            main_scenes=[
                Scene(
                    scene_description="Scene 1 description",
                    visual_prompt="Scene 1 visual prompt"
                ),
                Scene(
                    scene_description="Scene 2 description",
                    visual_prompt="Scene 2 visual prompt"
                )
            ]
        )

        # Mock other service responses
        mock_generate_image.return_value = "http://example.com/image.jpg"
        mock_generate_voice.return_value = "http://example.com/voice.mp3"
        mock_generate_music.return_value = "http://example.com/music.mp3"
        mock_generate_video.return_value = "http://example.com/video.mp4"

        result = content_creation_worker(
            template_name="basic",
            run_parameters={
                "scene_amount": 2,
                "generate_image": True,
                "generate_voice": True,
                "generate_music": True,
                "generate_video": True
            },
            variable_inputs=[{"name": "Test Subject"}],
            app=self.app
        )

        self.assertEqual(len(result), 1)
        content = result[0]
        self.assertEqual(content['title'], "The Life of Test Subject")
        self.assertEqual(content['description'], "A fascinating video about Test Subject")
        self.assertEqual(len(content['scenes']), 2)
        self.assertEqual(content['image_url'], "http://example.com/image.jpg")
        self.assertEqual(content['voice_url'], "http://example.com/voice.mp3")
        self.assertEqual(content['music_url'], "http://example.com/music.mp3")
        self.assertEqual(content['video_url'], "http://example.com/video.mp4")

        mock_generate_content.assert_called_once()
        mock_generate_image.assert_called_once()
        mock_generate_voice.assert_called_once()
        mock_generate_music.assert_called_once()
        mock_generate_video.assert_called_once()

if __name__ == '__main__':
    unittest.main()