from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy instance (this should be outside the create_app function)
db = SQLAlchemy()

# Function to initialize the core app
def create_app():
    app = Flask(__name__)

    # Configure app
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # Use SQLite for the database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking

    # Initialize the database with the app
    db.init_app(app)

    # Import and register blueprints or routes
    from .views import main_bp
    app.register_blueprint(main_bp)

    return app
