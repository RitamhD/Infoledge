from .auth_routes import auth_bp
from .home_routes import home_bp
from .chat_routes import chat_bp
from .code_routes import code_bp
from .course_routes import course_bp

__all__ = ["auth_bp", "home_bp", "chat_bp", "code_bp", "course_bp"]