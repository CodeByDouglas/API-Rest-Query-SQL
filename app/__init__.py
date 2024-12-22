from flask import Flask
from app.config import Config
from app.controllers.user_controller import user_bp 

def create_app():
    
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.register_blueprint(user_bp, url_prefix="/api")
    
    return app