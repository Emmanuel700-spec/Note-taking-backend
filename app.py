from flask import Flask, session, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, User  
from routes import api_bp
import logging
from flask_bcrypt import Bcrypt
from flask_mail import Mail

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)

    # Load configuration
    app.config.from_object('config.Config')  
    app.config['SECRET_KEY'] = 'f83e412280ce4cb1cf021835276930269087e08fc4251236'  
    app.config['SESSION_COOKIE_NAME'] = 'your_session_cookie'  
    app.config['SESSION_TYPE'] = 'filesystem' 

    # Initialize CORS with specific origin
    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

    # Initialize extensions
    db.init_app(app)
    bcrypt = Bcrypt(app)
    migrate = Migrate(app, db)
    mail = Mail(app)

    # Register the API blueprint
    app.register_blueprint(api_bp, url_prefix='/api')

    # Add a simple homepage route
    @app.route('/')
    def home():
        return "Welcome to the Note Taking App! The app is currently running."

    return app  

def setup_database(app):
    """Create the database tables if they don't exist."""
    with app.app_context():
        db.create_all()  

def run_app(app):
    """Run the Flask application."""
    app.run(host='0.0.0.0', port=5000, debug=True)  

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)  
    app = create_app()
    setup_database(app)  
    run_app(app)
