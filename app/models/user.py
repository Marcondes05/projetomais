from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    cpf = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # 'discente' ou 'docente'
    curso = db.Column(db.String(120), nullable=True)

    # Relacionamento com projetos onde é orientador
    projetos_orientados = db.relationship("Project", backref="orientador", lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"
