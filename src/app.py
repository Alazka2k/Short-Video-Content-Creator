import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize SQLAlchemy
db = SQLAlchemy()

def create_app():
    # Initialize Flask app
    app = Flask(__name__)

    # Log whether we're using the mock client
    app.logger.info(f"Using Mock LLM Client: {os.environ.get('USE_MOCK_LLM', 'false').lower() == 'true'}")

    # Configure SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///content_creation.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize SQLAlchemy with app
    db.init_app(app)

    # Import models and workers after db initialization to avoid circular imports
    from models import Content
    from workers import content_creation_worker

    @app.route('/create_content', methods=['POST'])
    def create_content():
        app.logger.info(f"Received request data: {request.json}")
        data = request.json

        # Validate request data
        if not all(key in data for key in ['initial_prompt', 'run_parameters', 'variable_inputs']):
            app.logger.warning("Request missing required fields")
            return jsonify({'error': 'Missing required fields'}), 400

        initial_prompt = data['initial_prompt']
        run_parameters = data['run_parameters']
        variable_inputs = data['variable_inputs']

        # Validate that 'name' is in variable_inputs
        if 'name' not in variable_inputs:
            app.logger.warning("Request missing 'name' field in variable_inputs")
            return jsonify({'error': 'Name is required in variable_inputs'}), 400

        try:
            app.logger.info(f"Generating content for name: {variable_inputs['name']}")
            result = content_creation_worker(initial_prompt, run_parameters, variable_inputs)
            if isinstance(result, dict) and 'error' in result:
                app.logger.error(f"Error in content generation: {result['error']}")
                return jsonify(result), 500
            app.logger.info(f"Generated result: {result}")
            return jsonify(result), 200
        except Exception as e:
            app.logger.error(f"Unexpected error in content_creation_worker: {str(e)}")
            return jsonify({'error': 'Internal server error'}), 500

    # Create tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    if not os.environ.get('ANTHROPIC_API_KEY'):
        logging.error("ANTHROPIC_API_KEY not set in environment variables")
        exit(1)
    
    app = create_app()
    app.run(debug=True)