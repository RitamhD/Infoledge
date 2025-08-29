import os
from datetime import timedelta
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

from .models.chat_model_setup import Model
from .models.recommender_model import Recommender

load_dotenv()

oauth = OAuth()
chat_model = Model()
recommender = Recommender()

db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()


def create_app():
    app = Flask(__name__, template_folder='view', static_folder='static')
    app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
    
    #------------------ Sessions -----------------------#    
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    
    #------------------ Database -----------------------#
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    bcrypt.init_app(app)
    
    #------------------ JWT -----------------------#
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    app.config['JWT_TOKEN_LOCATION'] = ["cookies"]
    app.config['JWT_COOKIE_SECURE'] = True     # True on HTTPS
    app.config['JWT_COOKIE_SAMESITE'] = "Lax"
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False   # True in production
    
    jwt.init_app(app)
    
    # ---------- JWT Error Handlers ----------
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
        return jsonify({"error": "login_required"}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        return jsonify({"error": "invalid_token"}), 401
    
    @jwt.expired_token_loader
    def expired_token_callback(callback):
        return jsonify({"error": "token_expired"}), 401
        
    
    #------------------ OAuth (Google) -----------------------#
    oauth.init_app(app=app)
    oauth.register("Infoledge",
                   client_id = os.getenv("OAUTH_CLIENT_ID"),
                   client_secret = os.getenv("OAUTH_CLIENT_SECRET_KEY"),
                   server_metadata_url = os.getenv("OAUTH_META_URL"),
                   client_kwargs = {"scope": "openid profile email"},
    )
    
    # Blueprints – imported from app/routes/__init__.py
    from .routes import auth_bp, home_bp, code_bp, course_bp, chat_bp, roadmap_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(code_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(roadmap_bp)
    
    # Create tables if not exists
    with app.app_context():
        db.create_all()
    
    return app
    
    