import os  # Import os to access environment variables
from models import db
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

# Import the blueprint from routes.py
from routes import api_bp

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Load configuration from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{os.environ.get('DB_USER')}:{os.environ.get('DB_PASSWORD')}@"
        f"{os.environ.get('DB_HOST')}/{os.environ.get('DB_NAME')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional, to suppress warnings

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-default-secret-key')  # Load from env or use a default
    app.config['SESSION_COOKIE_NAME'] = 'your_session_cookie'
    app.config['SESSION_TYPE'] = 'filesystem'

    # Initialize CORS with specific origin
    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

    
    db.init_app(app)
    bcrypt = Bcrypt(app)
    migrate = Migrate(app, db)

    
    app.register_blueprint(api_bp, url_prefix='/api')

    
    @app.route('/')
    def home():
        return "Welcome to the Note Taking App! The app is currently running."

    with app.app_context():
        db.create_all()  

    return app
