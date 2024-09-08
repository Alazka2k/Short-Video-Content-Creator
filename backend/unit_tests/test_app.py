# backend/unit_tests/test_app.py

import unittest
from unittest.mock import patch
from backend.src.app import create_app
from backend.src.prisma_client import get_prisma

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.prisma = get_prisma()
        if cls.prisma is None:
            raise Exception("Failed to initialize Prisma")

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @classmethod
    def tearDownClass(cls):
        if cls.prisma:
            cls.prisma.disconnect()

    @patch('app.content_creation_worker')
    @patch('app.prisma.connect')
    @patch('app.prisma.disconnect')
    def test_create_content(self, mock_disconnect, mock_connect, mock_worker):
        mock_worker.return_value = [{'id': 1, 'title': 'Test Title', 'description': 'Test Description'}]
        response = self.client.post('/api/create-content', json={
            'videoSubject': 'Test Subject',
            'generalOptions': {
                'style': 'Documentary',
                'description': 'A test video',
                'sceneAmount': 3,
                'duration': 60,
                'tone': 'Informative',
                'vocabulary': 'Simple',
                'targetAudience': 'General',
                'services': {
                    'generate_image': True,
                    'generate_voice': True,
                    'generate_music': False,
                    'generate_video': False
                }
            },
            'contentOptions': {
                'pacing': 'Moderate',
                'description': 'Test content description'
            },
            'visualPromptOptions': {
                'pictureDescription': 'Test picture',
                'style': 'Realistic',
                'imageDetails': 'Test details',
                'shotDetails': 'Close-up'
            }
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['title'], 'Test Title')
        self.assertEqual(data['description'], 'Test Description')

    @patch('app.prisma.content.find_unique')
    @patch('app.prisma.connect')
    @patch('app.prisma.disconnect')
    def test_get_content_progress(self, mock_disconnect, mock_connect, mock_find_unique):
        mock_find_unique.return_value = {
            'id': 1,
            'status': 'in_progress',
            'progress': 50,
            'currentStep': 'Generating images',
            'errorMessage': None
        }
        response = self.client.get('/api/content-progress/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['id'], 1)
        self.assertEqual(data['status'], 'in_progress')
        self.assertEqual(data['progress'], 50)
        self.assertEqual(data['currentStep'], 'Generating images')

    def test_health_check(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')

if __name__ == '__main__':
    unittest.main()