from pydantic import BaseModel
from typing import List

class Scene(BaseModel):
    scene_description: str
    visual_prompt: str

class VideoContent(BaseModel):
    video_title: str
    description: str
    main_scenes: List[Scene]
