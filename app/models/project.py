from app import db

project_students = db.Table('project_students',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('student_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
)

project_coorientadores = db.Table('project_coorientadores',
    db.Column('project_id', db.Integer, db.ForeignKey('projects.id'), primary_key=True),
    db.Column('coorientador_id', db.Integer, db.ForeignKey('usuarios.id'), primary_key=True)
)

class Project(db.Model):
    __tablename__ = "projects"
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    resumo = db.Column(db.Text)
    tipo = db.Column(db.String(50))
    edital = db.Column(db.String(120))
    ano = db.Column(db.String(10))
    financiador = db.Column(db.String(120))   # <- nome que usamos no form
    orientador_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"))
    orientador = db.relationship("User", foreign_keys=[orientador_id])
    estudantes = db.relationship("User", secondary=project_students, backref="projetos_estudante")
    coorientadores = db.relationship("User", secondary=project_coorientadores, backref="projetos_coorientador")

    def __repr__(self):
        return f"<Project {self.id} {self.titulo}>"
