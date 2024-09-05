# Short Video Content Creator

## Project Overview
The Short Video Content Creator is an automated system designed to generate engaging short videos about notable figures in science and technology. This project leverages various AI services to create content, images, audio, and video, streamlining the process of educational video production.

## Key features include:
- Automated content generation using OpenAI's GPT model
- Image generation for video scenes
- Text-to-speech conversion for narration
- Background music generation
- Final video compilation
- Web-based user interface for content creation and management

## Current Status
As of September 04, 2024, the project has achieved the following milestones:

- Implemented core content generation functionality using OpenAI's GPT model
- Developed a Flask-based backend API for handling content creation requests
- Created a Next.js frontend with basic UI for video content creation
- Integrated mock implementations for image, voice, music, and video generation services
- Implemented a SQLite database for content storage
- Added configuration management with separate dev and prod config files
- Developed a robust testing framework including unit tests and an interactive test script
- Implemented error handling and logging throughout the application
- Set up CI/CD pipeline with GitHub Actions for automated testing

### Recent Updates
- Fixed issues in frontend tests, particularly in CreateContent.test.js
- Improved asynchronous handling in tests
- Resolved mocking issues for fetch and alert functions
- Updated test files to use userEvent for more realistic user interactions

### Next Steps
1. Replace mock implementations with actual AI services for image, voice, music, and video generation
2. Enhance the frontend UI/UX
3. Implement user authentication and authorization
4. Conduct comprehensive end-to-end testing
5. Optimize performance and implement scalability measures
6. Resolve remaining issues in CreateContent component tests
7. Implement progress tracking for long-running processes
8. Improve multi-entry processing capability
9. Update documentation to reflect recent changes and new features

## Project Structure

```
SHORT-VIDEO-CONTENT-CREATOR/
├── .github/
│   └── workflows/
│       └── python-tests.yml
├── .pytest_cache/
├── .vscode/
├── docs/
│   ├── developer_guide.md
│   ├── installation_guide.md
│   ├── prompt_generator_docs.md
│   └── user_guide.md
├── examples/
│   └── prompt_generator_examples.py
├── frontend/
│   ├── .next/
│   ├── __tests__/
│   ├── components/
│   ├── node_modules/
│   ├── pages/
│   │   └── api/
│   ├── public/
│   ├── styles/
│   └── ... (other frontend files)
├── src/
│   ├── __pycache__/
│   ├── instance/
│   ├── __init__.py
│   ├── app.py
│   ├── config-dev.yaml
│   ├── config-loader.py
│   ├── config-prod.yaml
│   ├── config.yaml
│   ├── content-creation.py
│   ├── models.py
│   ├── progress_tracker.py
│   ├── prompt_generator.py
│   ├── prompt_templates.yaml
│   ├── server.py
│   ├── services.py
│   └── workers.py
├── tests/
│   └── interactive_test.py
├── unit_tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_app.py
│   ├── test_content_creation.py
│   ├── test_models.py
│   ├── test_openai_connection.py
│   ├── test_openai_service.py
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

## Getting Started

For detailed information on how to install, use, and contribute to this project, please refer to the following documentation:

- [Installation Guide](docs/installation_guide.md)
- [User Guide](docs/user_guide.md)
- [Developer Guide](docs/developer_guide.md)

### Quick Start

1. Clone the repository and navigate to the project directory.
2. Set up the backend:
   a. Create and activate a virtual environment.
   b. Install backend dependencies with `pip install -r requirements.txt`.
   c. Set up your environment variables in a `.env` file.
   d. Run the server with `python src/server.py`.
3. Set up the frontend:
   a. Navigate to the `frontend` directory.
   b. Install frontend dependencies with `npm install`.
   c. Run the development server with `npm run dev`.

## Running Tests

To run backend tests:
```
python run_tests.py
```

To run frontend tests:
```
cd frontend
npm test
```

## Contributing

Contributions are welcome! Please read our [Developer Guide](docs/developer_guide.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.