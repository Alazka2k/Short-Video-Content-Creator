import logging
from prisma import Prisma
from .services import generate_content_with_openai, generate_image, generate_voice, generate_music, generate_video
from shared.types.ContentCreation import ContentCreationRequest, VideoContent
from typing import Dict, Any, List
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from .progress_tracker import ProgressTracker

prisma = Prisma()

class ContentCreationPipeline:
    def __init__(self, template_file: str):
        self.prompt_generator = PromptGenerator(template_file)
        self.logger = logging.getLogger(__name__)

    async def process_input(self, input_data: List[ContentCreationRequest]) -> List[Dict[str, Any]]:
        results = []
        total_entries = len(input_data)
        progress_tracker = ProgressTracker(total_entries * 6)  # 6 steps per entry

        with ThreadPoolExecutor() as executor:
            future_to_entry = {executor.submit(self.create_content, entry, index, total_entries, progress_tracker): entry for index, entry in enumerate(input_data, start=1)}
            for future in as_completed(future_to_entry):
                entry = future_to_entry[future]
                try:
                    result = await future.result()
                    results.append(result)
                except Exception as e:
                    self.logger.error(f"Error processing entry: {entry.videoSubject} - {str(e)}", exc_info=True)
                    results.append({"error": str(e), "videoSubject": entry.videoSubject})

        return results

    async def create_content(self, input_data: ContentCreationRequest, index: int, total_entries: int, progress_tracker: ProgressTracker) -> Dict[str, Any]:
        self.logger.info(f"Processing entry {index}/{total_entries}: {input_data.videoSubject}")
        base_step = (index - 1) * 6
        try:
            prompt = self.prompt_generator.generate_prompt("video_content", input_data.dict())
            generated_content: VideoContent = await generate_content_with_openai(prompt)
            progress_tracker.update(base_step + 1, {"videoSubject": input_data.videoSubject, "status": "content generated"})

            content = await self.save_to_database(generated_content, input_data)
            progress_tracker.update(base_step + 2, {"videoSubject": input_data.videoSubject, "status": "content saved"})
            
            if input_data.generalOptions.services.get('generate_image'):
                image_url = await generate_image(generated_content.description)
                await prisma.content.update(
                    where={"id": content.id},
                    data={"generatedPicture": image_url}
                )
                progress_tracker.update(base_step + 3, {"videoSubject": input_data.videoSubject, "status": "image generated"})
            
            if input_data.generalOptions.services.get('generate_voice'):
                voice_url = await generate_voice('\n'.join([scene.scene_description for scene in generated_content.main_scenes]))
                await prisma.content.update(
                    where={"id": content.id},
                    data={"generatedVoice": voice_url}
                )
                progress_tracker.update(base_step + 4, {"videoSubject": input_data.videoSubject, "status": "voice generated"})
            
            if input_data.generalOptions.services.get('generate_music'):
                music_url = await generate_music(f"Create {input_data.generalOptions.style} music for a video about {input_data.videoSubject}")
                await prisma.content.update(
                    where={"id": content.id},
                    data={"generatedMusic": music_url}
                )
                progress_tracker.update(base_step + 5, {"videoSubject": input_data.videoSubject, "status": "music generated"})
            
            if input_data.generalOptions.services.get('generate_video'):
                video_url = await generate_video(content.id)
                await prisma.content.update(
                    where={"id": content.id},
                    data={"generatedVideo": video_url, "status": "completed", "progress": 100}
                )
                progress_tracker.update(base_step + 6, {"videoSubject": input_data.videoSubject, "status": "video generated"})

            return content
        except Exception as e:
            self.logger.error(f"Error creating content for {input_data.videoSubject}: {str(e)}", exc_info=True)
            raise

    async def save_to_database(self, generated_content: VideoContent, input_data: ContentCreationRequest) -> Dict[str, Any]:
        try:
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
                        "create": [{"type": "scene", "sceneNumber": i+1, "description": scene.visual_description} 
                                   for i, scene in enumerate(generated_content.main_scenes)]
                    },
                    "musicPrompt": {
                        "create": {
                            "description": f"Create {input_data.generalOptions.style} music for a video about {input_data.videoSubject}"
                        }
                    }
                }
            )
            self.logger.info(f"Saved content to database for {input_data.videoSubject}")
            return content
        except Exception as e:
            self.logger.error(f"Error saving to database: {str(e)}", exc_info=True)
            raise

content_pipeline = ContentCreationPipeline("prompt_templates.yaml")

async def content_creation_worker(input_data: List[ContentCreationRequest]) -> List[Dict[str, Any]]:
    logger = logging.getLogger(__name__)
    logger.info(f"Starting content creation for {len(input_data)} entries")
    
    try:
        results = await content_pipeline.process_input(input_data)
        return results
    except Exception as e:
        logger.error(f"Error in content creation: {str(e)}", exc_info=True)
        return [{"error": f"Failed to generate content: {str(e)}"}]