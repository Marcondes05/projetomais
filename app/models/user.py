from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    cpf = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(200), unique=True, nullable=False)
    senha = db.Column(db.String(300), nullable=False)
    tipo = db.Column(db.String(30), nullable=False)  # 'discente' ou 'docente' ou 'tecnico'
    campus = db.Column(db.String(100), nullable=False)
    curso = db.Column(db.String(150), nullable=True)

    def set_password(self, raw):
        self.senha = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.senha, raw)

    def is_docente(self):
        return self.tipo and self.tipo.lower() in ("docente", "tecnico")

    def is_discente(self):
        return self.tipo and self.tipo.lower() == "discente"

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"{self.nome} - {self.email}"
