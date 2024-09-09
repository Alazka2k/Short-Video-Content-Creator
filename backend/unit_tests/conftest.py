# backend/unit_tests/conftest.py

import sys
import os
import pytest
import asyncio
from dotenv import load_dotenv

# Get the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

shared_dir = os.path.join(project_root, 'shared')
if os.path.exists(shared_dir):
    sys.path.insert(0, shared_dir)

# Load environment variables
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path)

# Construct the absolute path to the database file
db_path = os.path.join(project_root, 'shared', 'prisma', 'dev.db')
os.environ['DATABASE_URL'] = f"file:{db_path}"

# Import after setting up the path
from backend.src.config import load_config
from backend.src.prisma_client import init_prisma, disconnect_prisma
from backend.src.models import VideoContent, Scene

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def config():
    return load_config()

@pytest.fixture(scope="session")
async def prisma_client():
    prisma = await init_prisma()
    yield prisma
    await disconnect_prisma()

@pytest.fixture
def sample_video_content():
    return VideoContent(
        video_title="Sample Video",
        description="This is a sample video description",
        main_scenes=[
            Scene(scene_description="Scene 1 description", visual_prompt="Scene 1 visual prompt"),
            Scene(scene_description="Scene 2 description", visual_prompt="Scene 2 visual prompt")
        ]
    )