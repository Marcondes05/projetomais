from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.project import Project
from app.models.user import User
from app.utils.auth_utils import role_required

project_bp = Blueprint("project", __name__)


# ============================================================
# LISTAR PROJETOS COM FILTROS
# ============================================================
@project_bp.route("/projetos")
@login_required
def lista_projetos():

    titulo = request.args.get("titulo", "").strip()
    tipo = request.args.get("tipo", "").strip()
    ano = request.args.get("ano", "").strip()
    edital = request.args.get("edital", "").strip()
    orientador = request.args.get("orientador", "").strip()

    query = Project.query

    if titulo:
        query = query.filter(Project.titulo.ilike(f"%{titulo}%"))

    if tipo and tipo != "todos":
        query = query.filter(Project.tipo == tipo)

    if ano and ano.isdigit():
        query = query.filter(Project.ano == (ano))

    if edital:
        query = query.filter(Project.edital.ilike(f"%{edital}%"))

    if orientador.isdigit():
        query = query.filter(Project.orientador_id == int(orientador))

    projetos = query.order_by(Project.id.desc()).all()

    return render_template(
        "projetos_list.html",
        projetos=projetos,
        filtros={
            "titulo": titulo,
            "tipo": tipo,
            "ano": ano,
            "edital": edital,
            "orientador": orientador
        }
    )



# ============================================================
# AUTOCOMPLETE (JSON)
# ============================================================
@project_bp.route("/buscar-usuarios")
@login_required
def buscar_usuarios():
    termo = request.args.get("q", "").strip()

    if not termo:
        return jsonify([])

    usuarios = User.query.filter(
        (User.nome.ilike(f"%{termo}%")) |
        (User.email.ilike(f"%{termo}%"))
    ).limit(20).all()

    return jsonify([
        {"id": u.id, "nome": u.nome, "email": u.email}
        for u in usuarios
    ])


# ============================================================
# NOVO PROJETO — FORMULÁRIO
# ============================================================
@project_bp.route("/novo")
@login_required
@role_required("docente")
def novo_projeto():
    return render_template("project_form.html")


# ============================================================
# SALVAR NOVO PROJETO
# ============================================================
@project_bp.route("/salvar", methods=["POST"])
@login_required
@role_required("docente")
def salvar_projeto():

    orientador_id = request.form.get("orientador_id") or current_user.id

    projeto = Project(
        titulo=request.form.get("titulo"),
        resumo=request.form.get("resumo"),
        tipo=request.form.get("tipo"),
        edital=request.form.get("edital"),
        ano=request.form.get("ano"),
        financiador=request.form.get("financiador"),
        orientador_id=orientador_id
    )

    db.session.add(projeto)
    db.session.commit()

    # Estudantes
    estudantes_ids = request.form.get("estudantes_ids", "")
    if estudantes_ids.strip():
        ids = [int(i) for i in estudantes_ids.split(",") if i.isdigit()]
        projeto.estudantes = User.query.filter(User.id.in_(ids)).all()

    # Coorientadores
    coor_ids = request.form.get("coorientadores_ids", "")
    if coor_ids.strip():
        ids = [int(i) for i in coor_ids.split(",") if i.isdigit()]
        projeto.coorientadores = User.query.filter(User.id.in_(ids)).all()

    db.session.commit()

    flash("Projeto cadastrado com sucesso!", "success")
    return redirect(url_for("project.lista_projetos"))


# ============================================================
# MEUS PROJETOS
# ============================================================
@project_bp.route("/meus-projetos")
@login_required
def meus_projetos():

    # --- Recebendo filtros ---
    filtros = {
        "titulo": request.args.get("titulo", "").strip(),
        "ano": request.args.get("ano", "").strip(),
        "tipo": request.args.get("tipo", "").strip(),
        "edital": request.args.get("edital", "").strip(),
        "orientador": request.args.get("orientador", "").strip(),
    }

    query = Project.query

    # PROJETOS DO USUÁRIO LOGADO
    if current_user.tipo == "discente":
        query = query.join(Project.estudantes).filter(User.id == current_user.id)

    elif current_user.tipo == "docente":
        query = query.filter(
            (Project.orientador_id == current_user.id) |
            (Project.coorientadores.any(User.id == current_user.id))
        )

    # --- Aplicando filtros ---
    if filtros["titulo"]:
        query = query.filter(Project.titulo.ilike(f"%{filtros['titulo']}%"))

    if filtros["tipo"] and filtros["tipo"] != "todos":
        query = query.filter(Project.tipo == filtros["tipo"])

    if filtros["ano"]:
        query = query.filter(Project.ano == (filtros["ano"]))

    if filtros["edital"]:
        query = query.filter(Project.edital.ilike(f"%{filtros['edital']}%"))

    if filtros["orientador"]:
        query = query.filter(Project.orientador_id == int(filtros["orientador"]))

    projetos = query.order_by(Project.id.desc()).all()

    return render_template("meus_projetos.html", projetos=projetos, filtros=filtros)



# ============================================================
# VISUALIZAR PROJETO
# ============================================================
@project_bp.route("/ver/<int:project_id>")
@login_required
def ver_projeto(project_id):
    projeto = Project.query.get_or_404(project_id)
    return render_template("projeto_view.html", projeto=projeto)


# ============================================================
# EDITAR — FORMULÁRIO
# ============================================================
@project_bp.route("/editar/<int:project_id>")
@login_required
@role_required("docente")
def editar_projeto(project_id):

    projeto = Project.query.get_or_404(project_id)

    if current_user.id != projeto.orientador_id:
        flash("Somente o orientador pode editar este projeto.", "danger")
        return redirect(url_for("project.ver_projeto", project_id=project_id))

    return render_template("projeto_edit.html", projeto=projeto)


# ============================================================
# ATUALIZAR PROJETO
# ============================================================
@project_bp.route("/atualizar/<int:project_id>", methods=["POST"])
@login_required
@role_required("docente")
def atualizar_projeto(project_id):

    projeto = Project.query.get_or_404(project_id)

    if current_user.id != projeto.orientador_id:
        flash("Você não pode editar este projeto.", "danger")
        return redirect(url_for("project.ver_projeto", project_id=project_id))

    projeto.titulo = request.form.get("titulo")
    projeto.resumo = request.form.get("resumo")
    projeto.tipo = request.form.get("tipo")
    projeto.edital = request.form.get("edital")
    projeto.ano = request.form.get("ano")
    projeto.financiador = request.form.get("financiador")

    # estudante IDs
    estudantes_ids = request.form.get("estudantes_ids", "")
    if estudantes_ids.strip():
        ids = [int(i) for i in estudantes_ids.split(",") if i.isdigit()]
        projeto.estudantes = User.query.filter(User.id.in_(ids)).all()
    else:
        projeto.estudantes = []

    # coorientadores IDs
    coor_ids = request.form.get("coorientadores_ids", "")
    if coor_ids.strip():
        ids = [int(i) for i in coor_ids.split(",") if i.isdigit()]
        projeto.coorientadores = User.query.filter(User.id.in_(ids)).all()
    else:
        projeto.coorientadores = []

    # orientador pode mudar
    orientador_id = request.form.get("orientador_id")
    if orientador_id and orientador_id.isdigit():
        projeto.orientador_id = int(orientador_id)

    db.session.commit()

    flash("Projeto atualizado com sucesso!", "success")
    return redirect(url_for("project.ver_projeto", project_id=project_id))


# ============================================================
# CONFIRMAR EXCLUSÃO
# ============================================================
@project_bp.route("/excluir/<int:project_id>")
@login_required
@role_required("docente")
def confirmar_exclusao(project_id):

    projeto = Project.query.get_or_404(project_id)

    if current_user.id != projeto.orientador_id:
        flash("Somente o orientador pode excluir este projeto.", "danger")
        return redirect(url_for("project.ver_projeto", project_id=project_id))

    return render_template("projeto_delete_confirm.html", projeto=projeto)


# ============================================================
# EXCLUSÃO DEFINITIVA
# ============================================================
@project_bp.route("/excluir/<int:project_id>", methods=["POST"])
@login_required
@role_required("docente")
def excluir_projeto(project_id):

    projeto = Project.query.get_or_404(project_id)

    if current_user.id != projeto.orientador_id:
        flash("Somente o orientador pode excluir.", "danger")
        return redirect(url_for("project.ver_projeto", project_id=project_id))

    db.session.delete(projeto)
    db.session.commit()

    flash("Projeto excluído com sucesso!", "success")
    return redirect(url_for("project.lista_projetos"))
