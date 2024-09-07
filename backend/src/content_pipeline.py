import logging
from prisma import Prisma
from .services import generate_content_with_openai, generate_image, generate_voice, generate_music, generate_video
from shared.types.ContentCreation import ContentCreationRequest, VideoContent
from typing import Dict, Any, List
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from .progress_tracker import ProgressTracker

prisma = Prisma()

class PromptGenerator:
    def __init__(self, template_file: str):
        # Load templates from file
        self.templates = self.load_templates(template_file)

    def load_templates(self, template_file: str) -> Dict[str, str]:
        # Implement loading templates from file
        pass

    def generate_prompt(self, template_name: str, variables: Dict[str, Any]) -> str:
        if template_name not in self.templates:
            raise ValueError(f"Unknown template: {template_name}")
        
        template = self.templates[template_name]
        return template.format(**variables)

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
                    self.logger.error(f"Error processing entry: {entry.title} - {str(e)}", exc_info=True)
                    results.append({"error": str(e), "title": entry.title})

        return results

    async def create_content(self, input_data: ContentCreationRequest, index: int, total_entries: int, progress_tracker: ProgressTracker) -> Dict[str, Any]:
        self.logger.info(f"Processing entry {index}/{total_entries}: {input_data.title}")
        base_step = (index - 1) * 6
        try:
            prompt = self.prompt_generator.generate_prompt("video_content", input_data.dict())
            generated_content: VideoContent = await generate_content_with_openai(prompt)
            progress_tracker.update(base_step + 1, {"title": input_data.title, "status": "content generated"})

            processed_content = self.process_generated_content(generated_content, input_data)
            progress_tracker.update(base_step + 2, {"title": input_data.title, "status": "content processed"})
            
            # Generate additional content based on selected services
            if input_data.services.get('generate_image'):
                processed_content['image_url'] = await generate_image(processed_content['description'])
                progress_tracker.update(base_step + 3, {"title": input_data.title, "status": "image generated"})
            
            if input_data.services.get('generate_voice'):
                processed_content['voice_url'] = await generate_voice(processed_content['audio_narration'])
                progress_tracker.update(base_step + 4, {"title": input_data.title, "status": "voice generated"})
            
            if input_data.services.get('generate_music'):
                processed_content['music_url'] = await generate_music(f"Create {input_data.style} music for a video about {input_data.title}")
                progress_tracker.update(base_step + 5, {"title": input_data.title, "status": "music generated"})
            
            if input_data.services.get('generate_video'):
                processed_content['video_url'] = await generate_video(processed_content)
                progress_tracker.update(base_step + 6, {"title": input_data.title, "status": "video generated"})

            content = await self.save_to_database(processed_content, input_data)
            progress_tracker.update(base_step + 6, {"title": input_data.title, "status": "completed"})
            return content
        except Exception as e:
            self.logger.error(f"Error creating content for {input_data.title}: {str(e)}", exc_info=True)
            raise

    def process_generated_content(self, generated_content: VideoContent, input_data: ContentCreationRequest) -> Dict[str, Any]:
        return {
            'title': generated_content.video_title,
            'description': generated_content.description,
            'scenes': [scene.dict() for scene in generated_content.main_scenes],
            'audio_narration': '\n'.join([scene.scene_description for scene in generated_content.main_scenes])
        }

    async def save_to_database(self, processed_content: Dict[str, Any], input_data: ContentCreationRequest) -> Dict[str, Any]:
        try:
            content = await prisma.content.create(
                data={
                    "title": processed_content['title'],
                    "description": processed_content['description'],
                    "targetAudience": input_data.targetAudience,
                    "duration": input_data.duration,
                    "style": input_data.style,
                    "services": json.dumps(input_data.services),
                    "generatedContent": json.dumps(processed_content),
                    "status": "completed",
                    "progress": 100
                }
            )
            self.logger.info(f"Saved content to database for {input_data.title}")
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