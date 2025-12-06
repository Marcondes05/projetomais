# app/utils/auth_utils.py
from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user, login_required

def role_required(*allowed_roles):
    """
    Decorator to restrict access to users whose current_user.tipo
    is in allowed_roles. Use after @login_required.
    Example:
        @app.route("/projeto/novo")
        @login_required
        @role_required('docente', 'tecnico')
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("É necessário fazer login.", "warning")
                return redirect(url_for("auth.login"))
            # current_user.tipo expected to be a string like 'discente' / 'docente' / 'tecnico'
            if current_user.tipo not in allowed_roles:
                flash("Você não tem permissão para acessar esta página.", "danger")
                return redirect(url_for("main.home") if "main" in kwargs.get("blueprint", "") else url_for("auth.login"))
            return func(*args, **kwargs)
        return wrapper
    return decorator
