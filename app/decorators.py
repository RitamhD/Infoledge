from functools import wraps
from flask import session, redirect, url_for, flash



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user"):
            flash("Sign in required !!!")
            return redirect(url_for("auth.google_login"))
        return f(*args, **kwargs)
    return decorated_function