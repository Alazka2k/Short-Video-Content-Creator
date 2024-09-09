# backend/src/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from shared.types.ContentCreation import ContentCreationRequest, ContentCreationResponse
from backend.src.content_pipeline import content_creation_worker
import os
import yaml
import logging
from backend.src.config import load_config
from backend.src.prisma_client import get_prisma
import asyncio

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    config = load_config()
    app.config.update(config)
    
    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    prisma = None

    @app.before_request
    async def before_request():
        nonlocal prisma
        if prisma is None:
            prisma = await get_prisma()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        loop = asyncio.get_event_loop()
        if prisma:
            loop.run_until_complete(prisma.disconnect())

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

            results = await content_creation_worker(content_requests)
            
            # Assuming content_creation_worker returns a list of dictionaries
            response_data = [ContentCreationResponse(**result).dict() for result in results]
            
            # If it's a single item, return it directly; otherwise, return the list
            if len(response_data) == 1:
                return jsonify(response_data[0]), 201
            else:
                return jsonify(response_data), 201

        except Exception as e:
            logger.error(f"Error in content creation: {str(e)}", exc_info=True)
            return jsonify({'error': str(e)}), 500

    @app.route('/api/content-progress/<int:content_id>', methods=['GET'])
    async def get_content_progress(content_id):
        try:
            content = await prisma.content.find_unique(
                where={"id": content_id},
                select={
                    "id": True,
                    "status": True,
                    "progress": True,
                    "currentStep": True,
                    "errorMessage": True,
                }
            )
            if not content:
                return jsonify({'error': 'Content not found'}), 404

            return jsonify(content), 200
        except Exception as e:
            logger.error(f"Error fetching content progress: {str(e)}", exc_info=True)
            return jsonify({'error': 'An error occurred while fetching the content progress'}), 500

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy'}), 200

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)