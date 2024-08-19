# Short Video Content Creator

## Project Overview

The Short Video Content Creator is an automated system that generates engaging short videos about notable figures in science and technology. It uses various AI services to create content, images, audio, and video.

## Current Status

As of August 19, 2024, the project has achieved the following milestones:

- Implemented core content generation functionality using OpenAI's GPT model
- Developed a robust testing framework with unit tests covering key components
- Successfully integrated with a SQLite database for content storage
- Implemented a Flask-based web server for handling content creation requests
- Added configuration management with separate dev and prod config files
- Implemented prompt generation and template management
- Added comprehensive documentation for the Prompt Generation System

All tests are currently passing, indicating that the core functionality is working as expected.

## Project Structure

```
SHORT-VIDEO-CONTENT-CREATOR/
├── .github/
│   └── workflows/
├── .pytest_cache/
├── docs/
│   ├── prompt_generator_docs.md
│   ├── installation_guide.md
│   ├── user_guide.md
│   └── developer_guide.md
├── examples/
│   └── prompt_generator_examples.py
├── instance/
├── public/
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── config-dev.yaml
│   ├── config-loader.py
│   ├── config-prod.yaml
│   ├── config.yaml
│   ├── content-creation.py
│   ├── models.py
│   ├── prompt_generator.py
│   ├── prompt_templates.yaml
│   ├── server.py
│   ├── services.py
│   └── workers.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_app.py
│   ├── test_content_creation.py
│   ├── test_models.py
│   ├── test_openai_connection.py
│   ├── test_prompt_generator.py
│   ├── test_services.py
│   └── test_workers.py
├── .env
├── .env.example
├── .gitignore
├── .pre-commit-config.yaml
├── LICENSE
├── README.md
├── pytest.ini
├── requirements.txt
└── run_tests.py
```

## Documentation

For detailed information on how to install, use, and contribute to this project, please refer to the following documentation:

- [Installation Guide](docs/installation_guide.md): Step-by-step instructions for setting up the project.
- [User Guide](docs/user_guide.md): How to use the Short Video Content Creator.
- [Developer Guide](docs/developer_guide.md): Information for contributors and developers.
- [Prompt Generation System Documentation](docs/prompt_generator_docs.md): Comprehensive guide on the Prompt Generation System.

## Quick Start

For a quick start, follow these steps:

1. Clone the repository and navigate to the project directory.
2. Create and activate a virtual environment.
3. Install dependencies with `pip install -r requirements.txt`.
4. Set up your environment variables in a `.env` file.
5. Run the server with `python src/server.py`.

For more detailed instructions, please refer to the [Installation Guide](docs/installation_guide.md).

## Running Tests

To run all tests:

```
python run_tests.py
```

## Contributing

Contributions are welcome! Please read our [Developer Guide](docs/developer_guide.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.