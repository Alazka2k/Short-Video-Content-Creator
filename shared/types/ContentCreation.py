from pydantic import BaseModel
from typing import List

class GeneralOptions(BaseModel):
    style: str
    description: str
    sceneAmount: int
    duration: int
    tone: str
    vocabulary: str
    targetAudience: str
    services: dict

class ContentOptions(BaseModel):
    pacing: str
    description: str

class VisualPromptOptions(BaseModel):
    pictureDescription: str
    style: str
    imageDetails: str
    shotDetails: str

class ContentCreationRequest(BaseModel):
    videoSubject: str
    generalOptions: GeneralOptions
    contentOptions: ContentOptions
    visualPromptOptions: VisualPromptOptions

class ContentCreationResponse(BaseModel):
    id: int
    title: str
    videoSubject: str
    status: str
    progress: float
    currentStep: str | None
    generatedContent: str
    generalOptions: GeneralOptions
    contentOptions: ContentOptions
    visualPromptOptions: VisualPromptOptions
    scenes: list
    visualPrompts: list
    audioPrompts: list
    musicPrompt: dict
    generatedPicture: str | None
    generatedVoice: str | None
    generatedMusic: str | None
    generatedVideo: str | None
    errorMessage: str | None
    createdAt: str
    updatedAt: str

class Scene(BaseModel):
    scene_description: str
    visual_description: str

class VideoContent(BaseModel):
    video_title: str
    description: str
    main_scenes: List[Scene]