from functools import wraps

from flask import abort, flash, redirect, url_for
from flask_login import current_user


def role_required(*roles):
    """Restrict a view to one or more user roles (e.g. 'owner', 'admin')."""

    def decorator(view_func):
        @wraps(view_func)
        def wrapped(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("auth.login"))
            if current_user.role not in roles:
                flash("You don't have permission to view that page.", "warning")
                return abort(403)
            return view_func(*args, **kwargs)

        return wrapped

    return decorator


def admin_required(view_func):
    return role_required("admin")(view_func)
