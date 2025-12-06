from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

# Página padrão quando o usuário tenta acessar algo sem login
login_manager.login_view = "auth.login"
login_manager.login_message = "Por favor, faça login para acessar esta página."


def create_app():
    app = Flask(
        __name__,
        static_folder="static",
        template_folder="templates"
    )
    app.config.from_object(Config)

    # Inicializa banco e login
    db.init_app(app)
    login_manager.init_app(app)

    # Importa os models
    from app.models.user import User
    from app.models.project import Project

    # Importa blueprints
    from app.routes.main_routes import main_bp
    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import user_bp
    from app.routes.project_routes import project_bp

    # Registra rotas principais
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(project_bp, url_prefix="/project")

    # Necessário para manter o usuário logado
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Cria tabelas caso ainda não existam
    with app.app_context():
        db.create_all()

    return app
