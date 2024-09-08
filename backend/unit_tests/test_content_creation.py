# backend/unit_tests/test_content_creation.py

import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(current_dir), 'src')
sys.path.insert(0, src_dir)

from backend.src.content_pipeline import ContentCreationPipeline, content_creation_worker
from backend.src.models import VideoContent, Scene
from backend.src.prisma_client import init_prisma
from shared.types.ContentCreation import ContentCreationRequest, GeneralOptions, ContentOptions, VisualPromptOptions

prisma = init_prisma()

class TestContentCreation(unittest.TestCase):
    def setUp(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        template_path = os.path.join(current_dir, "..", "src", "prompt_templates.yaml")
        self.pipeline = ContentCreationPipeline(template_path)

    @patch('content_pipeline.generate_content_with_openai')
    @patch('content_pipeline.generate_image')
    @patch('content_pipeline.generate_voice')
    @patch('content_pipeline.generate_music')
    @patch('content_pipeline.generate_video')
    @patch('content_pipeline.prisma.content.create')
    @patch('content_pipeline.prisma.content.update')
    async def test_content_creation(self, mock_update, mock_create, mock_generate_video, 
                                    mock_generate_music, mock_generate_voice, 
                                    mock_generate_image, mock_generate_content):
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

        # Mock database operations
        mock_create.return_value = MagicMock(id=1)
        mock_update.return_value = MagicMock(id=1)

        request = ContentCreationRequest(
            videoSubject="Test Subject",
            generalOptions=GeneralOptions(
                style="Documentary",
                description="A test video",
                sceneAmount=2,
                duration=60,
                tone="Informative",
                vocabulary="Simple",
                targetAudience="General",
                services={
                    "generate_image": True,
                    "generate_voice": True,
                    "generate_music": True,
                    "generate_video": True
                }
            ),
            contentOptions=ContentOptions(
                pacing="Moderate",
                description="Test content description"
            ),
            visualPromptOptions=VisualPromptOptions(
                pictureDescription="Test picture",
                style="Realistic",
                imageDetails="Test details",
                shotDetails="Close-up"
            )
        )

        result = await self.pipeline.create_content(request)

        self.assertEqual(result.title, "The Life of Test Subject")
        self.assertEqual(result.videoSubject, "Test Subject")
        self.assertEqual(len(result.scenes), 2)
        self.assertEqual(result.generatedPicture, "http://example.com/image.jpg")
        self.assertEqual(result.generatedVoice, "http://example.com/voice.mp3")
        self.assertEqual(result.generatedMusic, "http://example.com/music.mp3")
        self.assertEqual(result.generatedVideo, "http://example.com/video.mp4")

        mock_generate_content.assert_called_once()
        mock_generate_image.assert_called_once()
        mock_generate_voice.assert_called_once()
        mock_generate_music.assert_called_once()
        mock_generate_video.assert_called_once()
        mock_create.assert_called_once()
        self.assertEqual(mock_update.call_count, 4)  # One update for each generated asset

    @patch('content_pipeline.ContentCreationPipeline.create_content')
    async def test_content_creation_worker(self, mock_create_content):
        mock_create_content.return_value = {"id": 1, "title": "Test Video"}
        
        request = ContentCreationRequest(
            videoSubject="Test Subject",
            generalOptions=GeneralOptions(
                style="Documentary",
                description="A test video",
                sceneAmount=2,
                duration=60,
                tone="Informative",
                vocabulary="Simple",
                targetAudience="General",
                services={
                    "generate_image": True,
                    "generate_voice": True,
                    "generate_music": True,
                    "generate_video": True
                }
            ),
            contentOptions=ContentOptions(
                pacing="Moderate",
                description="Test content description"
            ),
            visualPromptOptions=VisualPromptOptions(
                pictureDescription="Test picture",
                style="Realistic",
                imageDetails="Test details",
                shotDetails="Close-up"
            )
        )

        result = await content_creation_worker([request])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 1)
        self.assertEqual(result[0]["title"], "Test Video")

        mock_create_content.assert_called_once()

if __name__ == '__main__':
    unittest.main()