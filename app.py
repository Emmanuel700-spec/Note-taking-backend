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
    
    with app.app_context():
        db.create_all()  

    return app  

 

if __name__ == '__main__':
    # Run locally using flask run
    app = create_app()
    app.run()
else:
    #run using gunucorn gunicorn -b 0.0.0.0:5000 app:gunicorn_app
    gunicorn_app = create_app()