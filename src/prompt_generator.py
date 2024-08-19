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
        self.templates = self._load_templates(template_file)
        self.components = self._load_components()

    def _load_templates(self, template_file: str) -> Dict[str, Dict[str, Any]]:
        """
        Load prompt templates from a YAML file.
        
        :param template_file: Path to the YAML file containing prompt templates.
        :return: Dictionary of loaded templates.
        :raises: Exception if the file cannot be loaded or parsed.
        """
        try:
            with open(template_file, 'r') as file:
                templates = yaml.safe_load(file)
            self.logger.info(f"Loaded {len(templates)} templates from {template_file}")
            return templates
        except Exception as e:
            self.logger.error(f"Failed to load template file: {e}")
            raise

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

    def generate_prompt(self, template_name: str, variables: Dict[str, Any]) -> str:
        """
        Generate a prompt using a specified template and variables.
        
        :param template_name: Name of the template to use.
        :param variables: Dictionary of variables to fill in the template.
        :return: Generated prompt string.
        :raises: ValueError if the template is not found.
        """
        if template_name not in self.templates:
            raise ValueError(f"Template '{template_name}' not found")

        template_data = self.templates[template_name]
        template = Template(template_data['template'])
        
        try:
            expanded_template = self._expand_components(template.safe_substitute(variables))
            prompt = Template(expanded_template).safe_substitute(variables)
            self.logger.info(f"Generated prompt for template '{template_name}'")
            return prompt
        except KeyError as e:
            self.logger.error(f"Missing variable in template: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Failed to generate prompt: {e}")
            raise

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