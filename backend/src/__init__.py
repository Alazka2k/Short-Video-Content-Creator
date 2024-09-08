# backend/src/__init__.py

from .config import load_config, validate_config
from .prisma_client import init_prisma
from .app import create_app
from .content_pipeline import ContentCreationPipeline, content_creation_worker
from .content_creation import ContentCreator, create_content
from .services import VideoScript, Scene, generate_content_with_openai, load_config
from .prompt_generator import PromptGenerator
from .progress_tracker import ProgressTracker

# Remove the import for models as we're now using Prisma
# from .models import db, Content

# You can add any other necessary imports or initialization code here

__all__ = [
    'create_app',
    'ContentCreationPipeline',
    'content_creation_worker',
    'ContentCreator',
    'create_content',
    'VideoScript',
    'Scene',
    'generate_content_with_openai',
    'generate_image',
    'generate_voice',
    'generate_music',
    'generate_video',
    'PromptGenerator',
    'ProgressTracker',
    'load_config',
    'init_prisma'
]