from pydantic import BaseModel
from typing import List, Optional

class GeneralOptions(BaseModel):
    style: str
    description: str
    sceneAmount: int
    duration: int
    tone: str
    vocabulary: str
    targetAudience: str

class ContentOptions(BaseModel):
    pacing: str
    description: str

class VisualPromptOptions(BaseModel):
    pictureDescription: str
    style: str
    imageDetails: str
    shotDetails: str

class Scene(BaseModel):
    type: str
    description: str

class AudioPrompt(BaseModel):
    type: str
    sceneNumber: int
    description: str

class VisualPrompt(BaseModel):
    type: str
    sceneNumber: int
    description: str

class MusicPrompt(BaseModel):
    description: str

class ContentCreationRequest(BaseModel):
    title: str
    videoSubject: str
    generalOptions: GeneralOptions
    contentOptions: ContentOptions
    visualPromptOptions: VisualPromptOptions

class ContentResponse(BaseModel):
    id: int
    title: str
    videoSubject: str
    status: str
    progress: float
    currentStep: Optional[str]
    generatedContent: Optional[str]
    generatedPicture: Optional[str]
    generatedVoice: Optional[str]
    generatedMusic: Optional[str]
    generatedVideo: Optional[str]
    createdAt: str
    updatedAt: str
    generalOptions: Optional[GeneralOptions]
    contentOptions: Optional[ContentOptions]
    visualPromptOptions: Optional[VisualPromptOptions]
    scenes: List[Scene]
    audioPrompts: List[AudioPrompt]
    visualPrompts: List[VisualPrompt]
    musicPrompt: Optional[MusicPrompt]