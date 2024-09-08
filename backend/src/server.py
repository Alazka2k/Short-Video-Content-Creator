# backend/src/server.py
from flask import Flask
from app import create_app

if __name__ == '__main__':
    app = create_app()
    print("Server is running. Access it at http://localhost:5000")
    print("Press CTRL+C to stop the server.")
    app.run(debug=True)