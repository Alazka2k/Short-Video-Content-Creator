import unittest
from unittest.mock import patch
import os
import sys

# Add the src directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(os.path.dirname(current_dir), 'src')
sys.path.insert(0, src_dir)

from app import create_app
from models import db

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    @patch('app.content_creation_worker')
    def test_create_content(self, mock_worker):
        mock_worker.return_value = {'title': 'Test Title', 'description': 'Test Description'}
        response = self.client.post('/create_content', json={
            'template_name': 'basic',
            'run_parameters': {'scene_amount': 5},
            'variable_inputs': {'name': 'Test Name'}
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('title', response.json)
        self.assertIn('description', response.json)

if __name__ == '__main__':
    unittest.main()