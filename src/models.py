# src/models.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Content(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    scenes = db.relationship('Scene', backref='content', lazy=True)

class Scene(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content_id = db.Column(db.Integer, db.ForeignKey('content.id'), nullable=False)
    description = db.Column(db.Text, nullable=False)
    visual_prompt = db.Column(db.Text, nullable=False)
    audio_script = db.Column(db.Text, nullable=True)