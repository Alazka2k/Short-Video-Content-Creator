import json
import os
import logging
from typing import Dict, Any, Optional, List
from .prompt_generator import PromptGenerator
from .services import generate_content_with_openai, generate_image, generate_voice, generate_music, generate_video
from prisma import Prisma
from shared.types.ContentCreation import ContentCreationRequest, VideoContent
from .progress_tracker import ProgressTracker

prisma = Prisma()

class ContentCreator:
    def __init__(self, template_file: str, test_input_file: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.prompt_generator = PromptGenerator(template_file)
        self.test_input = self.load_test_input(test_input_file) if test_input_file else None

    def load_test_input(self, test_input_file: str) -> Dict[str, Any]:
        with open(test_input_file, 'r') as file:
            lines = file.readlines()
        inputs = [line.strip() for line in lines]
        return {
            "name": inputs[0],
            "description": inputs[1],
            "target_audience": inputs[2],
            "video_length": int(inputs[3]),
            "image_style": inputs[4],
            "scene_amount": int(inputs[5])
        }

    async def create_content(self, input_data: ContentCreationRequest, is_test: bool = False, progress_tracker: Optional[ProgressTracker] = None) -> Dict[str, Any]:
        try:
            # Merge input_data with test_input if in test mode
            if is_test and self.test_input:
                merged_input = {**self.test_input, **input_data.dict()}
            else:
                merged_input = input_data.dict()

            if progress_tracker:
                progress_tracker.update(1, {"status": "Generating content prompt"})

            # Generate content prompt
            content_prompt = self.prompt_generator.generate_prompt("video_content", **merged_input)
            
            if progress_tracker:
                progress_tracker.update(2, {"status": "Generating content with OpenAI"})

            # Generate content using OpenAI
            generated_content: VideoContent = await generate_content_with_openai(content_prompt)

            if progress_tracker:
                progress_tracker.update(3, {"status": "Creating Content object"})

            # Create Content object using Prisma
            content = await prisma.content.create(
                data={
                    "title": generated_content.video_title,
                    "description": generated_content.description,
                    "targetAudience": merged_input['targetAudience'],
                    "duration": merged_input['duration'],
                    "style": merged_input['style'],
                    "services": json.dumps(merged_input['services']),
                    "generatedContent": generated_content.json(),
                    "status": "pending",
                    "progress": 0
                }
            )

            if progress_tracker:
                progress_tracker.update(4, {"status": "Content creation completed"})

            return content

        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON: {str(e)}")
            raise Exception(f"Error decoding JSON: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error in content creation pipeline: {str(e)}")
            raise

    def save_debug_info(self, title: str, data: Dict[str, Any]):
        debug_folder = f"debug/content/{title}"
        os.makedirs(debug_folder, exist_ok=True)
        
        with open(f"{debug_folder}/generated_content.json", "w") as f:
            json.dump(data, f, indent=2)

    async def process_batch(self, input_data_list: List[ContentCreationRequest], is_test: bool = False) -> List[Dict[str, Any]]:
        results = []
        total_entries = len(input_data_list)
        progress_tracker = ProgressTracker(total_entries * 5)  # 5 steps per entry

        for index, input_data in enumerate(input_data_list, start=1):
            try:
                content = await self.create_content(input_data, is_test, progress_tracker)
                results.append(content)
            except Exception as e:
                self.logger.error(f"Error processing entry {index}: {str(e)}")
                results.append({"error": str(e), "index": index})

        return results

# Make sure to export the class at the end of the file
__all__ = ['ContentCreator']

# Helper function to create content (now supports batch processing)
async def create_content(input_data: List[ContentCreationRequest], is_test: bool = False) -> List[Dict[str, Any]]:
    creator = ContentCreator("prompt_templates.yaml", "test_input.txt" if is_test else None)
    return await creator.process_batch(input_data, is_test)