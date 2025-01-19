from flask import Flask
from app.routes import main as routes

def create_app():
    app = Flask(__name__)
    return app