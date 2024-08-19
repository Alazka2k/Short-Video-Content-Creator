import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(current_dir), 'src')
sys.path.insert(0, src_dir)

from src.workers import content_creation_worker
from src.app import create_app, db

class TestContentCreation(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch('src.workers.generate_content_with_openai')  # Change this line
    def test_content_creation(self, mock_generate_content):
        mock_generate_content.return_value = "Test content"

        result = content_creation_worker(
            template_name="basic",
            run_parameters={"scene_amount": 5},
            variable_inputs={"name": "Test Subject"},
            app=self.app
        )

        self.assertIn('title', result)
        self.assertIn('description', result)
        mock_generate_content.assert_called_once()

if __name__ == '__main__':
    unittest.main()