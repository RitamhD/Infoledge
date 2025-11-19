import os
from datetime import timedelta
<<<<<<< HEAD
from flask import Flask, jsonify, render_template, redirect, url_for, flash
=======
from flask import Flask, jsonify, render_template, redirect
>>>>>>> 5f0416db394212f08a47de8aa1e66ce78c310935
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

<<<<<<< HEAD
from .models.chatbot_folder.chat_model_setup import Model
=======
from .models.chat_model_setup import Model
>>>>>>> 5f0416db394212f08a47de8aa1e66ce78c310935
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
<<<<<<< HEAD
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
=======
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
>>>>>>> 5f0416db394212f08a47de8aa1e66ce78c310935
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    bcrypt.init_app(app)
    
    #------------------ JWT -----------------------#
    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    app.config['JWT_TOKEN_LOCATION'] = ["cookies"]
<<<<<<< HEAD
    app.config["JWT_ACCESS_COOKIE_NAME"] = "access_token_cookie"
    app.config["JWT_REFRESH_COOKIE_NAME"] = "refresh_token_cookie"
=======
>>>>>>> 5f0416db394212f08a47de8aa1e66ce78c310935
    app.config['JWT_COOKIE_SECURE'] = False     # True on HTTPS
    app.config['JWT_COOKIE_SAMESITE'] = "Lax"
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False   # True in production
    
    jwt.init_app(app)
    
    # ---------- JWT Error Handlers ----------
    @jwt.unauthorized_loader
    def unauthorized_callback(callback):
<<<<<<< HEAD
        flash("Login required", "warning")
        return redirect(url_for('auth.landing_page'))
    
    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        return jsonify({"error": "invalid_token"})
    
    @jwt.expired_token_loader
    def expired_token_callback(callback):
        flash("Login required", "warning")
        return redirect(url_for('auth.landing_page'))
=======
        return jsonify({"error": "login_required"}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(callback):
        return jsonify({"error": "invalid_token"}), 401
    
    @jwt.expired_token_loader
    def expired_token_callback(callback):
        return redirect('auth.landing_page'), 401
        
>>>>>>> 5f0416db394212f08a47de8aa1e66ce78c310935
    
    #------------------ OAuth (Google) -----------------------#
    oauth.init_app(app=app)
    oauth.register("Infoledge",
                   client_id = os.getenv("OAUTH_CLIENT_ID"),
                   client_secret = os.getenv("OAUTH_CLIENT_SECRET_KEY"),
                   server_metadata_url = os.getenv("OAUTH_META_URL"),
                   client_kwargs = {"scope": "openid profile email"},
    )
    
    #------------------ 404 Error Handler -------------------------#
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    
    
<<<<<<< HEAD
    # Blueprints imported from app/routes/__init__.py
=======
    # Blueprints – imported from app/routes/__init__.py
>>>>>>> 5f0416db394212f08a47de8aa1e66ce78c310935
    from .routes import auth_bp, home_bp, code_bp, course_bp, chat_bp, roadmap_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(code_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(roadmap_bp)
    
<<<<<<< HEAD
    # Importing database models
    from app.models.user import User
    from app.models.chatbot_folder.chats import ChatSession
    from app.models.roadmaps_folder.roadmaps import Roadmap
=======
>>>>>>> 5f0416db394212f08a47de8aa1e66ce78c310935
    
    # Create tables if not exists
    with app.app_context():
        db.create_all()
    
    return app
    
    