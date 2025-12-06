from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.project import Project
from app.models.user import User
from app.utils.auth_utils import role_required

project_bp = Blueprint("project", __name__)

# -----------------------------
# LISTAR TODOS OS PROJETOS
# -----------------------------
@project_bp.route("/projetos")
@login_required
def lista_projetos():
    projetos = Project.query.order_by(Project.id.desc()).all()
    return render_template("projetos_list.html", projetos=projetos)


# -----------------------------
# FORMULÁRIO DE NOVO PROJETO
# -----------------------------
@project_bp.route("/novo")
@login_required
@role_required("docente")
def novo_projeto():
    return render_template(
        "project_form.html",
        alunos=User.query.filter_by(tipo="discente").all(),
        docentes=User.query.filter_by(tipo="docente").all()
    )


# -----------------------------
# SALVAR PROJETO
# -----------------------------
@project_bp.route("/salvar", methods=["POST"])
@login_required
@role_required("docente")
def salvar_projeto():

    titulo = request.form.get("titulo")
    resumo = request.form.get("resumo")
    tipo = request.form.get("tipo")
    edital = request.form.get("edital")
    ano = request.form.get("ano")
    financiador = request.form.get("financiador")

    estudantes_ids = request.form.get("estudantes_ids", "")
    coorientadores_ids = request.form.get("coorientadores_ids", "")

    estudantes_ids = [int(x) for x in estudantes_ids.split(",") if x.strip().isdigit()]
    coorientadores_ids = [int(x) for x in coorientadores_ids.split(",") if x.strip().isdigit()]

    projeto = Project(
        titulo=titulo,
        resumo=resumo,
        tipo=tipo,
        edital=edital,
        ano=int(ano),
        financiador=financiador,
        orientador_id=current_user.id
    )

    db.session.add(projeto)
    db.session.commit()

    # ---- Associar estudantes ----
    for est_id in estudantes_ids:
        estudante = User.query.get(est_id)
        if estudante:
            projeto.estudantes.append(estudante)

    # ---- Associar coorientadores ----
    for coo_id in coorientadores_ids:
        coor = User.query.get(coo_id)
        if coor:
            projeto.coorientadores.append(coor)

    db.session.commit()

    flash("Projeto cadastrado com sucesso!", "success")
    return redirect(url_for("project.lista_projetos"))


# -----------------------------
# AUTOCOMPLETE (JSON)
# -----------------------------
@project_bp.route("/buscar-usuarios")
@login_required
def buscar_usuarios():
    termo = request.args.get("q", "")
    if not termo:
        return jsonify([])

    usuarios = User.query.filter(
        (User.nome.ilike(f"%{termo}%")) |
        (User.email.ilike(f"%{termo}%"))
    ).all()

    return jsonify([{
        "id": u.id,
        "nome": u.nome,
        "email": u.email
    } for u in usuarios])



# -----------------------------
# MEUS PROJETOS
# -----------------------------
@project_bp.route("/meus-projetos")
@login_required
def meus_projetos():

    # Se discente → listar projetos onde ele está em estudantes
    if current_user.tipo == "discente":
        projetos = Project.query \
            .join(Project.estudantes) \
            .filter(User.id == current_user.id) \
            .order_by(Project.id.desc()) \
            .all()

    # Se docente → listar projetos onde ele orienta ou coorienta
    elif current_user.tipo == "docente":
        projetos = Project.query.filter(
            (Project.orientador_id == current_user.id) |
            (Project.coorientadores.any(User.id == current_user.id))
        ).order_by(Project.id.desc()).all()

    else:
        projetos = []

    return render_template("meus_projetos.html", projetos=projetos)
