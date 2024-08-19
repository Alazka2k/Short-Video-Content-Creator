# Installation Guide

This guide provides detailed steps to install and set up the Short Video Content Creator project.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## Step-by-Step Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/short-video-content-creator.git
   cd short-video-content-creator
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Set up environment variables:
   - Copy the `.env.example` file to `.env`:
     ```
     cp .env.example .env
     ```
   - Open the `.env` file and fill in your API keys and other necessary variables.

6. Initialize the database:
   ```
   python src/models.py
   ```

7. Run the tests to ensure everything is set up correctly:
   ```
   python run_tests.py
   ```

## Troubleshooting

If you encounter any issues during installation, please check the following:

- Ensure you're using the correct Python version (3.8+)
- Make sure all required system libraries are installed
- Check that your API keys in the `.env` file are correct

If problems persist, please open an issue on the GitHub repository.

## Next Steps

After installation, refer to the User Guide for information on how to use the Short Video Content Creator.