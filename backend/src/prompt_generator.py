# src/prompt_generator.py

import yaml
import logging
from string import Template
from typing import Dict, Any, List
import re

class PromptGenerator:
    def __init__(self, template_file: str):
        """
        Initialize the PromptGenerator with a template file.
        
        :param template_file: Path to the YAML file containing prompt templates.
        """
        self.logger = logging.getLogger(__name__)
        self.logger.info(f"Loading templates from: {template_file}")
        with open(template_file, 'r') as file:
            self.templates = yaml.safe_load(file)
        self.logger.info(f"Loaded templates: {list(self.templates.keys())}")

    def _load_components(self) -> Dict[str, str]:
        """
        Load reusable components for prompt templates.
        
        :return: Dictionary of component names and their content.
        """
        # This is a placeholder implementation. In a real-world scenario,
        # components might be loaded from a file or database.
        return {
            "greeting": "Hello, {name}!",
            "closing": "Thank you for using our service.",
        }

    def generate_prompt(self, template_name: str, **kwargs) -> str:
        """
        Generate a prompt using a specified template and variables.
        
        :param template_name: Name of the template to use.
        :param kwargs: Dictionary of variables to fill in the template.
        :return: Generated prompt string.
        :raises: ValueError if the template is not found.
        """
        self.logger.info(f"Generating prompt for template: {template_name}")
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found. Available templates: {list(self.templates.keys())}")
        template = self.templates[template_name]['template']
        
        # Filter kwargs to only include keys that are in the template
        filtered_kwargs = {k: v for k, v in kwargs.items() if f"{{{k}}}" in template}
        
        # Log any unused kwargs
        unused_kwargs = set(kwargs.keys()) - set(filtered_kwargs.keys())
        if unused_kwargs:
            self.logger.warning(f"Unused kwargs for template '{template_name}': {unused_kwargs}")
        
        return template.format(**filtered_kwargs)

    def _expand_components(self, template: str) -> str:
        """
        Expand component placeholders in a template.
        
        :param template: Template string potentially containing component placeholders.
        :return: Template string with component placeholders expanded.
        """
        for component_name, component_template in self.components.items():
            placeholder = f"{{component:{component_name}}}"
            if placeholder in template:
                template = template.replace(placeholder, component_template)
        return template

    def validate_prompt(self, prompt: str, template_name: str) -> bool:
        """
        Validate a generated prompt.
        
        :param prompt: The prompt to validate.
        :param template_name: Name of the template used to generate the prompt.
        :return: True if the prompt is valid, False otherwise.
        """
        if not prompt.strip():
            self.logger.warning("Generated prompt is empty")
            return False
        
        if re.search(r'\{[^}]+\}', prompt):
            self.logger.warning(f"Prompt for '{template_name}' contains unfilled placeholders")
            return False
        
        max_length = self.templates[template_name].get('max_length', 1000)
        if len(prompt) > max_length:
            self.logger.warning(f"Prompt for '{template_name}' exceeds maximum length of {max_length} characters")
            return False
        
        return True

    def get_required_variables(self, template_name: str) -> List[str]:
        """
        Get the list of required variables for a template.
        
        :param template_name: Name of the template.
        :return: List of variable names required by the template.
        :raises: ValueError if the template is not found.
        """
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        template = self.templates[template_name]['template']
        return re.findall(r'\$(\w+)', template)

    def add_template(self, name: str, template: str, max_length: int = 1000):
        """
        Add a new template to the PromptGenerator.
        
        :param name: Name of the new template.
        :param template: Template string.
        :param max_length: Maximum allowed length for prompts generated from this template.
        """
        self.templates[name] = {
            'template': template,
            'max_length': max_length
        }
        self.logger.info(f"Added new template: {name}")

    def remove_template(self, name: str):
        """
        Remove a template from the PromptGenerator.
        
        :param name: Name of the template to remove.
        """
        if name in self.templates:
            del self.templates[name]
            self.logger.info(f"Removed template: {name}")
        else:
            self.logger.warning(f"Attempted to remove non-existent template: {name}")