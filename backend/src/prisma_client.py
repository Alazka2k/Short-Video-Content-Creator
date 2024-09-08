import os
from dotenv import load_dotenv
from prisma import Prisma
from backend.src.config import load_config, validate_config, get_api_keys
import asyncio
import logging

# Laden Sie die .env-Datei aus dem Hauptverzeichnis
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(dotenv_path)

# Laden Sie die Konfiguration
config = load_config()
validate_config(config)

# Laden Sie die API-Schlüssel
api_keys = get_api_keys()

_prisma_instance = None

async def init_prisma():
    global _prisma_instance
    if _prisma_instance is None:
        _prisma_instance = Prisma()
        await _prisma_instance.connect()
    return _prisma_instance

def get_prisma():
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(init_prisma())

# Debug-Ausgaben
print(f"Current working directory: {os.getcwd()}")
print(f".env file exists: {os.path.exists(dotenv_path)}")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
print(f"Loaded config: {config}")
print(f"Database URL: {config['database']['url']}")
print(f"API Keys: {api_keys}")  # Neue Debug-Ausgabe für die API-Schlüssel