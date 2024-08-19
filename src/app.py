from flask import Flask, request, jsonify
from models import db
from workers import content_creation_worker

def create_app(config_name=None):
    app = Flask(__name__)
    
    if config_name == 'testing':
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///content_creation.db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/create_content', methods=['POST'])
    def create_content():
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        template_name = data.get('template_name')
        run_parameters = data.get('run_parameters', {})
        variable_inputs = data.get('variable_inputs', {})

        if not all([template_name, run_parameters, variable_inputs]):
            return jsonify({'error': 'Missing required fields'}), 400

        result = content_creation_worker(template_name, run_parameters, variable_inputs)
        return jsonify(result)

    return app

# This part is optional, but can be useful for running the app directly
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)