from pydantic import BaseModel
from typing import List
from backend.src.prisma_client import init_prisma

prisma = init_prisma()

# Hier sollte kein 'db = prisma()' sein, da prisma bereits initialisiert ist

class Scene(BaseModel):
    scene_description: str
    visual_prompt: str

class VideoContent(BaseModel):
    video_title: str
    description: str
    main_scenes: List[Scene]
