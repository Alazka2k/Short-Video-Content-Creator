# tests/test_app.py

import json
from flask import Flask
from src.app import create_app

def test_create_content_endpoint():
    app = create_app()
    client = app.test_client()

    data = {
        "initial_prompt": "Create a video script",
        "run_parameters": {
            "scene_amount": 3,
            "video_length": 60,
            "image_style": "Realistic"
        },
        "variable_inputs": {
            "name": "Albert Einstein"
        }
    }

    response = client.post('/create_content', 
                           data=json.dumps(data),
                           content_type='application/json')
    
    assert response.status_code == 200
    assert 'Video Title' in response.json
    assert 'Description' in response.json
    assert 'Hashtags' in response.json