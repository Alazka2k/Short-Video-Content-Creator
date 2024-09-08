import sys
import os

# Fügen Sie das Hauptverzeichnis des Projekts zum Python-Pfad hinzu
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)

# Fügen Sie auch das 'shared' Verzeichnis hinzu, falls es nicht im Hauptverzeichnis enthalten ist
shared_dir = os.path.join(project_root, 'shared')
if os.path.exists(shared_dir):
    sys.path.insert(0, shared_dir)

from backend.src import VideoScript, Scene, generate_content_with_openai, load_config
from backend.src.prisma_client import get_prisma

@pytest.fixture(scope="session")
def config():
    return load_config()

@pytest.fixture(scope="session")
def prisma():
    return get_prisma()