# backend/src/prompt_generator.py

import yaml
import logging
from typing import Dict, Any, List
import re

class PromptGenerator:
    def __init__(self, template_file: str):
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Loading templates from: {template_file}")
        with open(template_file, 'r') as file:
            self.templates = yaml.safe_load(file)
        self.logger.info(f"Loaded templates: {list(self.templates.keys())}")
        self.components = {}  # Initialize components dictionary

    def generate_prompt(self, template_name: str, data: Dict[str, Any]) -> str:
        self.logger.info(f"Generating prompt for template: {template_name}")
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found. Available templates: {list(self.templates.keys())}")
        
        template = self.templates[template_name]['template']
        
        # Expand components
        template = self._expand_components(template)
        
        # Flatten the nested dictionary
        flat_data = self._flatten_dict(data)
        
        # Fill in the template
        try:
            filled_template = template.format(**flat_data)
        except KeyError as e:
            self.logger.error(f"Missing key in data: {e}")
            raise ValueError(f"Missing data for key: {e}")
        
        return filled_template

    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)

    def validate_prompt(self, prompt: str, template_name: str) -> bool:
        if not prompt.strip():
            return False
        if '{' in prompt or '}' in prompt:
            return False
        # Add more validation logic if needed
        return True

    def get_required_variables(self, template_name: str) -> List[str]:
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        template = self.templates[template_name]['template']
        return re.findall(r'\{(\w+)\}', template)

    def add_template(self, name: str, template: str):
        self.templates[name] = {'template': template}
        self.logger.info(f"Added new template: {name}")

    def remove_template(self, name: str):
        if name in self.templates:
            del self.templates[name]
            self.logger.info(f"Removed template: {name}")
        else:
            self.logger.warning(f"Attempted to remove non-existent template: {name}")

    def _expand_components(self, template: str) -> str:
        for component_name, component_template in self.components.items():
            placeholder = f"{{component:{component_name}}}"
            if placeholder in template:
                template = template.replace(placeholder, component_template)
        return template