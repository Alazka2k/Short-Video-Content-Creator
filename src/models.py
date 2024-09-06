from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    target_audience = db.Column(db.String(100), nullable=True)
    duration = db.Column(db.Integer, nullable=False)
    style = db.Column(db.String(50), nullable=False)
    services = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    generated_content = db.Column(db.Text, nullable=True)
    generated_picture = db.Column(db.String(200), nullable=True)
    generated_voice = db.Column(db.String(200), nullable=True)
    generated_music = db.Column(db.String(200), nullable=True)
    generated_video = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f'<Content {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'target_audience': self.target_audience,
            'duration': self.duration,
            'style': self.style,
            'services': json.loads(self.services),
            'created_at': self.created_at.isoformat(),
            'generated_content': self.generated_content,
            'generated_picture': self.generated_picture,
            'generated_voice': self.generated_voice,
            'generated_music': self.generated_music,
            'generated_video': self.generated_video
        }