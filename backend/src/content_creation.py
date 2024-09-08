# backend/src/content_creation.py

import json
import logging
from typing import Dict, Any, Optional, List
from backend.src.prompt_generator import PromptGenerator
from backend.src.services import generate_content_with_openai, generate_image, generate_voice, generate_music, generate_video
from shared.types.ContentCreation import ContentCreationRequest, VideoContent
from backend.src.progress_tracker import ProgressTracker
from backend.src.prisma_client import init_prisma

prisma = init_prisma()

class ContentCreator:
    def __init__(self, template_file: str):
        self.logger = logging.getLogger(__name__)
        self.prompt_generator = PromptGenerator(template_file)

    async def create_content(self, input_data: ContentCreationRequest, progress_tracker: Optional[ProgressTracker] = None) -> Dict[str, Any]:
        try:
            if progress_tracker:
                progress_tracker.update(1, {"status": "Generating content prompt"})

            content_prompt = self.prompt_generator.generate_prompt("video_content", **input_data.dict())
            
            if progress_tracker:
                progress_tracker.update(2, {"status": "Generating content with OpenAI"})

            generated_content: VideoContent = await generate_content_with_openai(content_prompt)

            if progress_tracker:
                progress_tracker.update(3, {"status": "Creating Content object"})

            content = await prisma.content.create(
                data={
                    "title": generated_content.video_title,
                    "videoSubject": input_data.videoSubject,
                    "status": "pending",
                    "progress": 0,
                    "generatedContent": json.dumps(generated_content.dict()),
                    "generalOptions": {
                        "create": {
                            "style": input_data.generalOptions.style,
                            "description": input_data.generalOptions.description,
                            "sceneAmount": input_data.generalOptions.sceneAmount,
                            "duration": input_data.generalOptions.duration,
                            "tone": input_data.generalOptions.tone,
                            "vocabulary": input_data.generalOptions.vocabulary,
                            "targetAudience": input_data.generalOptions.targetAudience
                        }
                    },
                    "contentOptions": {
                        "create": {
                            "pacing": input_data.contentOptions.pacing,
                            "description": input_data.contentOptions.description
                        }
                    },
                    "visualPromptOptions": {
                        "create": {
                            "pictureDescription": input_data.visualPromptOptions.pictureDescription,
                            "style": input_data.visualPromptOptions.style,
                            "imageDetails": input_data.visualPromptOptions.imageDetails,
                            "shotDetails": input_data.visualPromptOptions.shotDetails
                        }
                    },
                    "scenes": {
                        "create": [{"type": "main", "description": scene.scene_description} for scene in generated_content.main_scenes]
                    },
                    "audioPrompts": {
                        "create": [{"type": "narration", "sceneNumber": i+1, "description": scene.scene_description} 
                                   for i, scene in enumerate(generated_content.main_scenes)]
                    },
                    "visualPrompts": {
                        "create": [{"type": "scene", "sceneNumber": i+1, "description": scene.visual_prompt} 
                                   for i, scene in enumerate(generated_content.main_scenes)]
                    },
                    "musicPrompt": {
                        "create": {
                            "description": f"Create {input_data.generalOptions.style} music for a video about {input_data.videoSubject}"
                        }
                    }
                }
            )

            if progress_tracker:
                progress_tracker.update(4, {"status": "Content creation completed"})

            return content

        except Exception as e:
            self.logger.error(f"Error in content creation pipeline: {str(e)}")
            raise

    async def process_batch(self, input_data_list: List[ContentCreationRequest]) -> List[Dict[str, Any]]:
        results = []
        total_entries = len(input_data_list)
        progress_tracker = ProgressTracker(total_entries * 5)  # 5 steps per entry

        for index, input_data in enumerate(input_data_list, start=1):
            try:
                content = await self.create_content(input_data, progress_tracker)
                results.append(content)
            except Exception as e:
                self.logger.error(f"Error processing entry {index}: {str(e)}")
                results.append({"error": str(e), "index": index})

        return results

async def create_content(input_data: List[ContentCreationRequest]) -> List[Dict[str, Any]]:
    creator = ContentCreator("prompt_templates.yaml")
    return await creator.process_batch(input_data)