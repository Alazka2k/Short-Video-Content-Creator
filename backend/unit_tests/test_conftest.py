# backend/unit_tests/test_conftest.py

import pytest
from backend.src.models import VideoContent, Scene
import logging
import uuid
logging.basicConfig(level=logging.DEBUG)

def test_config_fixture(config):
    assert config is not None
    assert isinstance(config, dict)
    assert 'database' in config

@pytest.mark.asyncio
async def test_prisma_fixture(prisma_client):
    assert prisma_client is not None
    # Try a simple database operation
    try:
        # Create a user first
        email = f"test-{uuid.uuid4()}@example.com"
        data = {
            "name": "Test User",
            "email": email,
            "password": "testpassword"
        }
        logging.debug(f"Attempting to create user with data: {data}")
        user = await prisma_client.user.create(data=data)
        assert user is not None
        assert user.name == 'Test User'

        # Now create a content associated with this user
        content_data = {
            'title': 'Test Content',
            'videoSubject': 'Test Subject',
            'userId': user.id,
            'status': 'pending'
        }
        logging.debug(f"Attempting to create content with data: {content_data}")
        content = await prisma_client.content.create(data=content_data)
        logging.debug(f"Content created: {content}")
        assert content is not None
        assert content.title == 'Test Content'
        assert content.userId == user.id

    except prisma.errors.PrismaError as e:
        logging.error(f"Prisma error occurred: {e}")
        pytest.fail(f"Failed to create content: {str(e)}")
    except Exception as e:
        logging.error(f"Unexpected error occurred: {e}")
        pytest.fail(f"Unexpected error: {str(e)}")
    finally:
        # Clean up
        try:
            if content:
                logging.debug(f"Attempting to delete content with id: {content.id}")
                await prisma_client.content.delete(where={"id": content.id})
            if user:
                logging.debug(f"Attempting to delete user with id: {user.id}")
                await prisma_client.user.delete(where={"id": user.id})
        except prisma.errors.PrismaError as e:
            logging.error(f"Prisma error occurred during cleanup: {e}")
        except Exception as e:
            logging.error(f"Unexpected error occurred during cleanup: {e}")

@pytest.mark.asyncio
async def test_database_connection(prisma_client):
    try:
        # Versuchen Sie eine einfache Datenbankabfrage durchzuführen
        result = await prisma_client.user.count()
        assert isinstance(result, int), "Die Abfrage sollte eine Ganzzahl zurückgeben"
        print(f"Anzahl der Benutzer in der Datenbank: {result}")
    except PrismaError as e:
        pytest.fail(f"Datenbankverbindung fehlgeschlagen: {str(e)}")

def test_sample_video_content_fixture(sample_video_content):
    assert sample_video_content is not None
    assert isinstance(sample_video_content, VideoContent)
    assert sample_video_content.video_title == "Sample Video"
    assert len(sample_video_content.main_scenes) == 2
    assert all(isinstance(scene, Scene) for scene in sample_video_content.main_scenes)