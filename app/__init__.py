from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    # IMPORTAR MODELS AQUI (obrigatório antes do create_all)
    from app.models.user import User
    from app.models.project import Project

    # CRIAR TABELAS NO BANCO (Supabase)
    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return "Hello World — Projetomais iniciado!"

    return app
