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
As of September 07, 2024, the project has achieved the following milestones:

- Implemented core content generation functionality using OpenAI's GPT model
- Developed a Flask-based backend API for handling content creation requests
- Created a Next.js frontend with basic UI for video content creation
- Integrated mock implementations for image, voice, music, and video generation services
- Implemented a Prisma ORM with SQLite database for content storage
- Added configuration management with separate dev and prod config files
- Developed a robust testing framework including unit tests and an interactive test script #need to be updated after changes
- Implemented error handling and logging throughout the application
- Set up CI/CD pipeline with GitHub Actions for automated testing ##currently deactivated
- Implemented progress tracking for long-running processes

## Project Structure

```
SHORT-VIDEO-CONTENT-CREATOR/
├── .github/
│   └── workflows/
│       └── python-tests.yml
├── docs/
│   ├── developer_guide.md
│   ├── installation_guide.md
│   ├── prompt_generator_docs.md
│   └── user_guide.md
├── frontend/
│   ├── __tests__/
│   ├── components/
│   │   ├── ContentCreationForm.js  # Form for creating new content
│   │   ├── Layout.js               # Main layout component
│   │   └── ProgressBar.js          # Progress indicator for content creation
│   ├── hooks/
│   │   ├── useForm.js              # Custom hook for form handling
│   │   └── useProgress.js          # Custom hook for progress tracking
│   ├── pages/
│   │   ├── api/
│   │   │   ├── content-progress.js # API route for content creation progress
│   │   │   ├── create-content.js   # API route for content creation
│   │   │   ├── create-video.js     # API route for video creation
│   │   │   └── get-content.js      # API route for fetching content
│   │   ├── _app.js                 # Next.js App component
│   │   ├── _document.js            # Next.js Document component
│   │   ├── content-result.js       # Page for displaying content creation results
│   │   ├── create-content.js       # Page for content creation form
│   │   ├── dashboard.js            # User dashboard page
│   │   └── index.js                # Home page
│   ├── utils/
│   │   └── api.js                  # Utility functions for API calls
│   └── styles/                     # CSS and styling files
├── backend/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── app.py                  # Main Flask application
│   │   ├── config-loader.py        # Configuration loading utility
│   │   ├── config.yaml             # Main configuration file
│   │   ├── content_creation.py     # Content creation logic
│   │   ├── content_pipeline.py     # Content processing pipeline
│   │   ├── models.py               # Database models (may be removed with Prisma)
│   │   ├── prisma.py               # Prisma ORM configuration
│   │   ├── progress_tracker.py     # Progress tracking utility
│   │   ├── prompt_generator.py     # Prompt generation for AI models
│   │   ├── prompt_templates.yaml   # Templates for AI prompts
│   │   ├── server.py               # Server startup script
│   │   └── services.py             # External services integration
│   ├── unit_tests/
│   │   ├── __init__.py
│   │   ├── conftest.py             # Test configuration
│   │   ├── test_app.py             # Tests for main application
│   │   ├── test_content_creation.py# Tests for content creation
│   │   ├── test_models.py          # Tests for database models
│   │   ├── test_openai_connection.py # Tests for OpenAI API connection
│   │   ├── test_openai_service.py  # Tests for OpenAI service
│   │   ├── test_prompt_generator.py# Tests for prompt generation
│   │   ├── test_services.py        # Tests for external services
│   │   └── test_workers.py         # Tests for background workers
│   ├── .env                        # Environment variables
│   └── requirements.txt            # Python dependencies
├── shared/
│   ├── prisma/
│   │   ├── migrations/             # Database migration files
│   │   ├── dev.db                  # Development SQLite database
│   │   └── schema.prisma           # Prisma schema file
│   └── types/
│       └── ContentCreation.ts      # Shared TypeScript types
├── .gitignore
├── LICENSE
├── README.md
└── run_tests.py                    # Script to run all tests
```

## Getting Started

For detailed information on how to install, use, and contribute to this project, please refer to the following documentation:

- [Installation Guide](docs/installation_guide.md)
- [User Guide](docs/user_guide.md)
- [Developer Guide](docs/developer_guide.md)

### Backend Quick Start

1. Clone the repository and navigate to the project directory.
2. Create and activate a virtual environment.
3. Navigate to the `backend` directory.
4. Install backend dependencies with `pip install -r requirements.txt`.
5. Set up your environment variables in the `backend/.env` file.
6. Run the server with `python src/server.py`.

### Frontend Quick Start

The frontend is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

1. Navigate to the `frontend` directory.
2. Install frontend dependencies with `npm install`.
3. Run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

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