import os
from dotenv import load_dotenv
from flask import Flask, request, current_app
from flask_cors import CORS
from flask_migrate import Migrate
from app.extensions import db, jwt, bcrypt, cors
from app.config import get_config
from app.routes import register_routes

# Load environment variables
load_dotenv()

if os.getenv('DATABASE_URI') is None:
    print("⚠️ Warning: DATABASE_URI not found in .env")
else:
    print(f"✅ DATABASE_URI found: {os.getenv('DATABASE_URI')}")

def create_app():
    """Factory function to create and configure the Flask app."""
    
    app = Flask(__name__)

    # Load Configuration
    app.config.from_object(get_config())

    # Secure CORS Configuration
    allowed_origins = os.getenv('ALLOWED_ORIGINS', '*')  
    cors.init_app(app, resources={r"/*": {"origins": allowed_origins.split(',')}})

    # Initialize Extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    migrate = Migrate(app, db)

    # Register Routes
    register_routes(app)

    # Import and register namespaces
    from app.routes.auth_routes import auth_ns
    from app.routes.admin_routes import admin_ns
    from app.routes.customer_routes import customer_ns
    from app.routes.driver_routes import driver_ns

    # Logging all incoming requests for debugging
    @app.before_request
    def log_request():
        current_app.logger.info(f'📥 Incoming {request.method} request to {request.path}')
        current_app.logger.info(f'🔐 Headers: {dict(request.headers)}')

        if request.method in ['POST', 'PUT', 'PATCH']:
            try:
                current_app.logger.info(f'📦 Request Body: {request.get_json()}')
            except Exception:
                current_app.logger.info(f'📦 Request Body: (unavailable)')

    return app
