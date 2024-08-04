# src/prompt_generator.py

import yaml
import logging
from string import Template
from typing import Dict, Any

class PromptGenerator:
    def __init__(self, template_file: str):
        self.templates = self._load_templates(template_file)
        self.logger = logging.getLogger(__name__)

    def _load_templates(self, template_file: str) -> Dict[str, str]:
        try:
            with open(template_file, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            self.logger.error(f"Failed to load template file: {e}")
            raise

    def generate_prompt(self, template_name: str, variables: Dict[str, Any]) -> str:
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")

        template = Template(self.templates[template_name]['template'])
        try:
            prompt = template.substitute(variables)
            self.logger.info(f"Generated prompt for template '{template_name}'")
            return prompt
        except KeyError as e:
            self.logger.error(f"Missing variable in template: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to generate prompt: {e}")
            raise

    def validate_prompt(self, prompt: str) -> bool:
        if not prompt.strip():
            self.logger.warning("Generated prompt is empty")
            return False
        return True