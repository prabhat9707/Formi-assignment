from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pathlib import Path

# Initialize Flask extensions
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    
    # Configure SQLite database
    base_dir = Path(__file__).resolve().parent.parent
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{base_dir}/properties.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from app.routes import api
    app.register_blueprint(api.bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app 