from flask import Flask, request, jsonify
from models import db, Content
from workers import content_creation_worker
from typing import List, Dict, Any
import yaml
import os

def load_config(config_file='config.yaml'):
    with open(config_file, 'r') as file:
        return yaml.safe_load(file)

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Load configuration
    config = load_config()
    
    if config_name == 'testing':
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = config['database']['url']
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.update(config)  # Add all config values to app.config
    
    db.init_app(app)

    @app.route('/api/create-content', methods=['POST'])
    def create_content():
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        required_fields = ['title', 'description', 'target_audience', 'duration', 'style', 'services']
        if not all(field in data for field in required_fields):
            return jsonify({'error': 'Missing required fields'}), 400

        try:
            content = Content(
                title=data['title'],
                description=data['description'],
                target_audience=data['target_audience'],
                duration=data['duration'],
                style=data['style'],
                services=str(data['services'])
            )
            db.session.add(content)
            db.session.commit()

            # Pass the configuration to the content_creation_worker
            result = content_creation_worker('basic', data, [{'name': data['title']}], app)
            
            if result and isinstance(result[0], dict) and 'error' not in result[0]:
                processed_content = result[0]
                # Update the content with the generated data
                content.generated_content = str(processed_content)
                db.session.commit()

                return jsonify({
                    'id': content.id,
                    'title': processed_content['title'],
                    'description': processed_content['description'],
                    'scenes': processed_content['scenes'],
                    'image_url': processed_content.get('image_url'),
                    'voice_url': processed_content.get('voice_url'),
                    'music_url': processed_content.get('music_url'),
                    'video_url': processed_content.get('video_url')
                }), 200
            else:
                error_message = result[0]['error'] if result and isinstance(result[0], dict) else 'Unknown error occurred'
                return jsonify({'error': error_message}), 500

        except Exception as e:
            app.logger.error(f"Error in content creation: {str(e)}")
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

    @app.route('/api/get-content/<int:content_id>', methods=['GET'])
    def get_content(content_id):
        try:
            content = Content.query.get(content_id)
            if not content:
                return jsonify({'error': 'Content not found'}), 404

            return jsonify(content.to_dict()), 200
        except Exception as e:
            app.logger.error(f"Error fetching content: {str(e)}")
            return jsonify({'error': str(e)}), 500

    @app.route('/health', methods=['GET'])
    def health_check():
        return jsonify({'status': 'healthy'}), 200

    return app

# This part is optional, but can be useful for running the app directly
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)