from flask import Blueprint, render_template
from flask_login import login_required, current_user

project_bp = Blueprint("project", __name__)

# ---------------------------
# LISTAGEM DE TODOS OS PROJETOS
# ---------------------------
@project_bp.route("/projetos")
@login_required
def lista_projetos():

    # Dados FICTÍCIOS (até construir o CRUD real)
    projetos_demo = [
        {
            "id": 1,
            "titulo": "Investigação do uso de IA no basquete",
            "aluno": "Marcondes Fernandes",
            "orientador": "Prof. Rodrigo Grassi",
            "ano": 2024
        },
        {
            "id": 2,
            "titulo": "IA na previsão de jogos de futebol",
            "aluno": "Pedro Henrique",
            "orientador": "Prof. Rodrigo Grassi",
            "ano": 2024
        }
    ]

    return render_template("projetos_list.html", projetos=projetos_demo)


# ---------------------------
# VISUALIZAR DETALHES (ainda simples)
# ---------------------------
@project_bp.route("/projeto/<int:project_id>")
@login_required
def view(project_id):
    return f"Página de detalhes do projeto {project_id} (implementação na Etapa 4)"
