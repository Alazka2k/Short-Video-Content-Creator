# Short Video Content Creator

## Project Overview

The Short Video Content Creator is an automated system that generates engaging short videos about notable figures in science and technology. It uses various AI services to create content, images, audio, and video.

## Current Status

As of August 21, 2024, the project has achieved the following milestones:

- Implemented core content generation functionality using OpenAI's GPT model
- Developed a robust testing framework with unit tests covering key components
- Successfully integrated with a SQLite database for content storage
- Implemented a Flask-based web server for handling content creation requests
- Added configuration management with separate dev and prod config files
- Implemented prompt generation and template management
- Created a Next.js frontend with a basic UI for video content creation
- Set up API routes for handling video creation requests
- Resolved several testing issues, particularly in frontend components

Most tests are currently passing, with a few remaining issues in the CreateContent component tests.

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
├── frontend/
│   ├── components/
│   ├── pages/
│   │   ├── api/
│   │   ├── create-content.js
│   │   └── content-result.js
│   ├── styles/
│   ├── __tests__/
│   │   ├── CreateContent.test.js
│   │   └── ContentResult.test.js
│   └── ... (other frontend files)
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

## Recent Updates

- Fixed issues in frontend tests, particularly in CreateContent.test.js
- Improved asynchronous handling in tests
- Resolved mocking issues for fetch and alert functions
- Updated test files to use userEvent for more realistic user interactions

## Next Steps

1. Resolve remaining issues in CreateContent component tests
2. Implement actual API integrations for image, voice, music, and video generation services
3. Enhance error handling and user feedback in the frontend
4. Implement progress tracking for long-running processes
5. Improve multi-entry processing capability
6. Conduct more comprehensive testing, including integration tests
7. Update documentation to reflect recent changes and new features

## Getting Started

For detailed information on how to install, use, and contribute to this project, please refer to the following documentation:

- [Installation Guide](docs/installation_guide.md)
- [User Guide](docs/user_guide.md)
- [Developer Guide](docs/developer_guide.md)

## Quick Start

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