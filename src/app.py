from flask import Flask, request, jsonify
from models import db, Content
from workers import content_creation_worker
from typing import List, Dict, Any

def create_app(config_name=None):
    app = Flask(__name__)
    
    if config_name == 'testing':
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///content_creation.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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

            result = content_creation_worker(content.id, data['services'])
            
            # Update the content with the generated data
            content.content = str(result)
            db.session.commit()

            return jsonify(result), 200
        except Exception as e:
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