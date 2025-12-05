from app import db
from datetime import datetime

# Tabela N:N para estudantes
projeto_estudantes = db.Table(
    "projeto_estudantes",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("projeto_id", db.Integer, db.ForeignKey("projetos.id")),
    db.Column("estudante_id", db.Integer, db.ForeignKey("usuarios.id")),
)

# Tabela N:N para coorientadores
projeto_coorientadores = db.Table(
    "projeto_coorientadores",
    db.Column("id", db.Integer, primary_key=True),
    db.Column("projeto_id", db.Integer, db.ForeignKey("projetos.id")),
    db.Column("coorientador_id", db.Integer, db.ForeignKey("usuarios.id")),
)

class Project(db.Model):
    __tablename__ = "projetos"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    resumo = db.Column(db.Text, nullable=True)
    edital = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(30), nullable=False)
    ano = db.Column(db.Integer, nullable=False)
    bolsa = db.Column(db.String(50), nullable=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    orientador_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)

    # N:N com estudantes
    estudantes = db.relationship(
        "User",
        secondary=projeto_estudantes,
        backref="projetos_participados",
        lazy="dynamic"
    )

    # N:N com coorientadores
    coorientadores = db.relationship(
        "User",
        secondary=projeto_coorientadores,
        backref="projetos_coorientados",
        lazy="dynamic"
    )

    def __repr__(self):
        return f"<Project {self.titulo}>"
