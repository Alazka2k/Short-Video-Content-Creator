from flask import Flask, request, jsonify
from flask_cors import CORS
from prisma import Prisma
from shared.types.ContentCreation import ContentCreationRequest, ContentCreationResponse
from .content_creation import create_content
import os
import yaml

prisma = Prisma()

def load_config():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(current_dir, 'config.yaml')
    
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def create_app(config_name=None):
    app = Flask(__name__)
    CORS(app)
    
    config = load_config()
    
    @app.before_request
    async def before_request():
        await prisma.connect()

    @app.teardown_appcontext
    async def shutdown_session(exception=None):
        await prisma.disconnect()

    @app.route('/api/create-content', methods=['POST'])
    async def create_content_endpoint():
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        try:
            if isinstance(data, list):
                content_requests = [ContentCreationRequest(**item) for item in data]
            else:
                content_requests = [ContentCreationRequest(**data)]

            results = await create_content(content_requests)
            
            return jsonify([ContentCreationResponse(**result).dict() for result in results]), 201
        except Exception as e:
            app.logger.error(f"Error in content creation: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/api/content-progress/<int:content_id>', methods=['GET'])
    async def get_content_progress(content_id):
        content = await prisma.content.find_unique(where={"id": content_id})
        if not content:
            return jsonify({'error': '