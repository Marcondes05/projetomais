from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager
from app.models.user import User

auth_bp = Blueprint("auth", __name__)

# Flask-Login: carregar usuário
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ----------------------------
# LOGIN
# ----------------------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        senha = request.form.get("senha")

        usuario = User.query.filter_by(email=email).first()

        if not usuario or not check_password_hash(usuario.senha, senha):
            flash("E-mail ou senha incorretos", "danger")
            return redirect(url_for("auth.login"))

        login_user(usuario)
        return redirect(url_for("main.home"))

    return render_template("login.html")

# ----------------------------
# REGISTRO
# ----------------------------
@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nome = request.form.get("nome")
        email = request.form.get("email")
        senha = request.form.get("senha")
        cpf = request.form.get("cpf")
        curso = request.form.get("curso")

        # Definir tipo pelo domínio
        if email.endswith("@estudante.iftm.edu.br"):
            tipo = "discente"
        elif email.endswith("@iftm.edu.br"):
            tipo = "docente"
        else:
            flash("Use um e-mail institucional válido!", "danger")
            return redirect(url_for("auth.registro"))

        senha_hash = generate_password_hash(senha)

        novo = User(
            nome=nome,
            email=email,
            senha=senha_hash,
            cpf=cpf,
            tipo=tipo,
            curso=curso if tipo == "discente" else None,
            campus=request.form.get("campus")
        )

        db.session.add(novo)
        db.session.commit()

        flash("Conta criada! Faça login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

# ----------------------------
# LOGOUT
# ----------------------------
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
