import os
from datetime import timedelta
from flask import Flask
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

from .models.chat_model_setup import Model
from .models.recommender_model import Recommender

load_dotenv()

oauth = OAuth()
chat_model = Model()
recommender = Recommender()

def create_app():
    app = Flask(__name__, template_folder='view', static_folder='static')
    app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    
#    #------------------OAuth setup-----------------------#
    oauth.init_app(app=app)
    oauth.register("Infoledge",
                   client_id = os.getenv("OAUTH_CLIENT_ID"),
                   client_secret = os.getenv("OAUTH_CLIENT_SECRET_KEY"),
                   client_metadata = os.getenv("OAUTH_META_URL"),
                   client_kwargs = {"scope": "openid profile email"},
    )
    
    from .routes import auth_bp, home_bp, code_bp, course_bp, chat_bp, roadmap_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(code_bp)
    app.register_blueprint(course_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(roadmap_bp)
    
    return app
    
    