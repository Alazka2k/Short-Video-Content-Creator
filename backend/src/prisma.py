import os
from dotenv import load_dotenv
from prisma import Prisma

# Load environment variables from .env file
load_dotenv()

# Set the PRISMA_SCHEMA_PATH environment variable to point to the shared schema
os.environ['PRISMA_SCHEMA_PATH'] = '../../shared/prisma/schema.prisma'

# Create a Prisma instance
prisma = Prisma()

# Function to initialize Prisma
async def init_prisma():
    await prisma.connect()

# Function to disconnect Prisma
async def disconnect_prisma():
    await prisma.disconnect()