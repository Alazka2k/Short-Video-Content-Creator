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
As of September 05, 2024, the project has achieved the following milestones:

- Implemented core content generation functionality using OpenAI's GPT model
- Developed a Flask-based backend API for handling content creation requests
- Created a Next.js frontend with basic UI for video content creation
- Integrated mock implementations for image, voice, music, and video generation services
- Implemented a SQLite database for content storage
- Added configuration management with separate dev and prod config files
- Developed a robust testing framework including unit tests and an interactive test script
- Implemented error handling and logging throughout the application
- Set up CI/CD pipeline with GitHub Actions for automated testing
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
├── examples/
│   └── prompt_generator_examples.py
├── frontend/
│   ├── __tests__/
│   ├── components/
│   │   ├── ContentCreationForm.js
│   │   ├── Layout.js
│   │   └── ProgressBar.js
│   ├── hooks/
│   │   ├── useForm.js
│   │   └── useProgress.js
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
│   ├── utils/
│   │   └── api.js
│   ├── styles/
│   └── ... (other frontend files)
├── src/
│   ├── __init__.py
│   ├── app.py
│   ├── config-dev.yaml
│   ├── config-loader.py
│   ├── config-prod.yaml
│   ├── config.yaml
│   ├── content_creation.py
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
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── run_tests.py
```

## Getting Started

For detailed information on how to install, use, and contribute to this project, please refer to the following documentation:

- [Installation Guide](docs/installation_guide.md)
- [User Guide](docs/user_guide.md)
- [Developer Guide](docs/developer_guide.md)

### Backend Quick Start

1. Clone the repository and navigate to the project directory.
2. Create and activate a virtual environment.
3. Install backend dependencies with `pip install -r requirements.txt`.
4. Set up your environment variables in a `.env` file.
5. Run the server with `python src/server.py`.

### Frontend Quick Start

The frontend is a [Next.js](https://nextjs.org/) project bootstrapped with [`create-next-app`](https://github.com/vercel/next.js/tree/canary/packages/create-next-app).

1. Navigate to the `frontend` directory.
2. Install frontend dependencies with `npm install`.
3. Run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `pages/index.js`. The page auto-updates as you edit the file.

[API routes](https://nextjs.org/docs/api-routes/introduction) can be accessed on [http://localhost:3000/api/hello](http://localhost:3000/api/hello). This endpoint can be edited in `pages/api/hello.js`.

The `pages/api` directory is mapped to `/api/*`. Files in this directory are treated as [API routes](https://nextjs.org/docs/api-routes/introduction) instead of React pages.

This project uses [`next/font`](https://nextjs.org/docs/basic-features/font-optimization) to automatically optimize and load Inter, a custom Google Font.

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

## Learn More About Next.js

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js/) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/deployment) for more details.

## Contributing

Contributions are welcome! Please read our [Developer Guide](docs/developer_guide.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.