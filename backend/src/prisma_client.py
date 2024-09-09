# backend/src/prisma_client.py

import os
from dotenv import load_dotenv
from prisma import Prisma
from backend.src.config import load_config, validate_config, get_api_keys
import asyncio
import logging
from functools import lru_cache

# Get the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

# Load the .env file from the project root
dotenv_path = os.path.join(project_root, '.env')
load_dotenv(dotenv_path)

# Construct the absolute path to the database file
db_path = os.path.join(project_root, 'shared', 'prisma', 'dev.db')
os.environ['DATABASE_URL'] = f"file:{db_path}"

# Load the configuration
config = load_config()
validate_config(config)

# Load the API keys
api_keys = get_api_keys()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@lru_cache()
def get_prisma():
    return Prisma()

async def init_prisma():
    prisma = get_prisma()
    try:
        if not prisma.is_connected():
            logger.debug("Connecting Prisma instance")
            await prisma.connect()
            logger.info("Prisma client connected.")
        return prisma
    except Exception as e:
        logger.error(f"Failed to initialize Prisma client: {str(e)}")
        raise

async def disconnect_prisma():
    prisma = get_prisma()
    if prisma.is_connected():
        await prisma.disconnect()
        logger.info("Prisma client disconnected.")

def print_debug_info():
    logger.debug(f"Current working directory: {os.getcwd()}")
    logger.debug(f".env file exists: {os.path.exists(dotenv_path)}")
    logger.debug(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
    logger.debug(f"Loaded config: {config}")
    logger.debug(f"Database URL: {config['database']['url']}")
    logger.debug(f"API Keys: {api_keys}")

# Print debug info
print_debug_info()