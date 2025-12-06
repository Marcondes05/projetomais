from flask import Blueprint, render_template
from flask_login import login_required, current_user

user_bp = Blueprint("user", __name__)

# ----------------------
# PERFIL DO USUÁRIO
# ----------------------
@user_bp.route("/perfil")
@login_required
def perfil():
    return render_template("perfil.html")


# ----------------------
# MEUS PROJETOS (fictício ainda)
# ----------------------
@user_bp.route("/meus-projetos")
@login_required
def meus_projetos():

    projetos_mock = [
        {
            "id": 1,
            "titulo": "Investigação do uso de IA no basquete",
            "orientador": "Prof. Rodrigo Grassi"
        }
    ]

    return render_template("meus_projetos.html", projetos=projetos_mock)
