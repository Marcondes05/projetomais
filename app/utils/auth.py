from flask import redirect, url_for, flash
from flask_login import current_user

def role_required(*roles):
    def wrapper(fn):
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("Faça login primeiro.", "warning")
                return redirect(url_for("auth.login"))

            if current_user.tipo not in roles:
                flash("Você não tem permissão para acessar esta página.", "danger")
                return redirect(url_for("home"))

            return fn(*args, **kwargs)
        decorated_view.__name__ = fn.__name__
        return decorated_view
    return wrapper
