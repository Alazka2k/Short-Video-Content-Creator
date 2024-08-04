# src/app.py

from flask import Flask, request, jsonify
from src.models import db
from src.workers import content_creation_worker

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///content_creation.db'
    db.init_app(app)

    @app.route('/create_content', methods=['POST'])
    def create_content():
        data = request.json
        if not all(key in data for key in ['initial_prompt', 'run_parameters', 'variable_inputs']):
            return jsonify({'error': 'Missing required fields'}), 400

        result = content_creation_worker(data['initial_prompt'], data['run_parameters'], data['variable_inputs'])
        if 'error' in result:
            return jsonify(result), 500
        return jsonify(result), 200

    @app.route('/get_content/<name>', methods=['GET'])
    def get_content(name):
        from src.models import Content
        content = Content.query.filter_by(name=name).first()
        if content:
            return jsonify({
                'name': content.name,
                'title': content.title,
                'description': content.description,
                'content': eval(content.content)
            }), 200
        return jsonify({'error': 'Content not found'}), 404

    return app