# backend/unit_tests/test_conftest.py

import pytest
from backend.src.models import VideoContent, Scene

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
        user = await prisma_client.user.create({
            'data': {
                'name': 'Test User',
                'email': 'test@example.com',
                'password': 'testpassword'  # In production, ensure this is hashed
            }
        })
        assert user is not None
        assert user.name == 'Test User'

        # Now create a content associated with this user
        content = await prisma_client.content.create({
            'data': {
                'title': 'Test Content',
                'videoSubject': 'Test Subject',
                'userId': user.id
            }
        })
        assert content is not None
        assert content.title == 'Test Content'
        assert content.userId == user.id

    except Exception as e:
        pytest.fail(f"Failed to create user or content: {str(e)}")
    finally:
        # Clean up
        if 'content' in locals():
            await prisma_client.content.delete({
                'where': {
                    'id': content.id
                }
            })
        if 'user' in locals():
            await prisma_client.user.delete({
                'where': {
                    'id': user.id
                }
            })

def test_sample_video_content_fixture(sample_video_content):
    assert sample_video_content is not None
    assert isinstance(sample_video_content, VideoContent)
    assert sample_video_content.video_title == "Sample Video"
    assert len(sample_video_content.main_scenes) == 2
    assert all(isinstance(scene, Scene) for scene in sample_video_content.main_scenes)