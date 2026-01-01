from api.auth_routes import auth_bp
from api.chat_routes import chat_bp

def register_blueprints(app):
    """Register all blueprints"""
    app.register_blueprint(auth_bp)
    app.register_blueprint(chat_bp)

