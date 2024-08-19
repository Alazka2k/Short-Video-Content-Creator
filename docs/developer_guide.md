# Developer Guide

This guide provides information for developers who want to contribute to or extend the Short Video Content Creator project.

## Project Structure

The project is organized as follows:

- `src/`: Contains the main source code
  - `app.py`: Flask application
  - `models.py`: Database models
  - `prompt_generator.py`: Prompt generation system
  - `services.py`: External API integrations
  - `workers.py`: Background task workers
- `tests/`: Contains all test files
- `docs/`: Project documentation
- `examples/`: Example scripts

## Setting Up the Development Environment

1. Follow the installation steps in the Installation Guide.

2. Install development dependencies:
   ```
   pip install -r requirements-dev.txt
   ```

3. Set up pre-commit hooks:
   ```
   pre-commit install
   ```

## Running Tests

Run all tests using:

```
python run_tests.py
```

To run a specific test file:

```
python -m unittest tests/test_prompt_generator.py
```

## Adding New Features

1. Create a new branch for your feature:
   ```
   git checkout -b feature/your-feature-name
   ```

2. Implement your feature, following the existing code style and structure.

3. Add tests for your new feature in the `tests/` directory.

4. Update documentation as necessary.

5. Run all tests to ensure nothing is broken.

6. Commit your changes and push to your fork.

7. Open a pull request with a clear description of your changes.

## Coding Standards

- Follow PEP 8 guidelines for Python code.
- Use type hints where possible.
- Write docstrings for all functions, classes, and modules.
- Maintain test coverage for all new code.

## Working with the Prompt Generation System

To extend the Prompt Generation System:

1. Add new templates to `src/prompt_templates.yaml`.
2. If needed, extend the `PromptGenerator` class in `src/prompt_generator.py`.
3. Add tests for new functionality in `tests/test_prompt_generator.py`.

## Continuous Integration

The project uses GitHub Actions for CI. Check `.github/workflows/` for the current CI configuration.

## Getting Help

If you need help or have questions about development, please open an issue on the GitHub repository or contact the project maintainers.