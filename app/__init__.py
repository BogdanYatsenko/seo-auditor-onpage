from flask import Flask
from .database import init_db
from .routes import bp as routes_bp
import os

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'dev-secret')
    init_db()
    app.register_blueprint(routes_bp)
    return app
