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
├── .pytest_cache/
├── .vscode/
├── backend/
│   ├── archive/
│   ├── src/
│   │   ├── __pycache__/
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── Backend Code.txt
│   │   ├── config-loader.py
│   │   ├── config.yaml
│   │   ├── content_creation.py
│   │   ├── content_pipeline.py
│   │   ├── models.py
│   │   ├── prisma_client.py
│   │   ├── progress_tracker.py
│   │   ├── prompt_generator.py
│   │   ├── prompt_templates.yaml
│   │   ├── server.py
│   │   └── services.py
│   ├── unit_tests/
│   │   ├── __pycache__/
│   │   ├── conftest.py
│   │   ├── test_app.py
│   │   ├── test_content_creation.py
│   │   ├── test_openai_connection.py
│   │   ├── test_openai_service.py
│   │   ├── test_prisma_import.py
│   │   ├── test_prompt_generator.py
│   │   └── test_services.py
│   ├── .env
│   └── requirements.txt
├── docs/
│   ├── developer_guide.md
│   ├── installation_guide.md
│   ├── prompt_generator_docs.md
│   └── user_guide.md
├── examples/
│   └── prompt_generator_examples.py
├── frontend/
│   ├── __tests__/
│   ├── .next/
│   ├── .swc/
│   ├── components/
│   │   ├── ContentCreationForm.js
│   │   ├── Layout.js
│   │   ├── Navbar.js
│   │   ├── ParameterTooltip.js
│   │   ├── ProgressBar.js
│   │   └── ResultDashboard.js
│   ├── hooks/
│   │   ├── useForm.js
│   │   └── useProgress.js
│   ├── lib/
│   │   └── contentCreation.js
│   ├── node_modules/
│   ├── pages/
│   │   ├── api/
│   │   │   ├── content-progress.js
│   │   │   ├── create-content.js
│   │   │   ├── create-video.js
│   │   │   └── get-content.js
│   │   ├── _app.js
│   │   ├── _document.js
│   │   ├── content-result.js
│   │   ├── create-content.js
│   │   ├── dashboard.js
│   │   └── index.js
│   ├── public/
│   ├── styles/
│   ├── utils/
│   │   ├── api.js
│   │   └── randomParameter.js
│   ├── .babelrc
│   ├── next.config.js
│   ├── package.json
│   └── tsconfig.json
├── instance/
│   └── content_creation.db
├── migrations/
├── public/
├── shared/
│   ├── prisma/
│   │   ├── migrations/
│   │   ├── dev.db
│   │   ├── dev.db-journal
│   │   └── schema.prisma
│   └── types/
│       ├── ContentCreation.py
│       └── ContentCreation.ts
├── .gitignore
├── LICENSE
├── README.md
└── run_tests.py
```

### Key components:

.github/workflows/: Contains CI/CD configuration for GitHub Actions.
backend/: Flask backend application.

src/: Main backend source code.
unit_tests/: Backend unit tests.


docs/: Project documentation.
examples/: Example scripts and usage.
frontend/: Next.js frontend application.

components/: React components.
hooks/: Custom React hooks.
pages/: Next.js pages and API routes.
utils/: Utility functions.


shared/: Shared resources between frontend and backend.

prisma/: Prisma ORM configuration and database.
types/: Shared type definitions.

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