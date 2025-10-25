import re
import requests
from flask import Blueprint, session, render_template, redirect, url_for, request, flash, jsonify
from app import oauth, db, bcrypt
from app.models.user import User
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    set_access_cookies, set_refresh_cookies,
    unset_jwt_cookies, jwt_required, get_jwt_identity,
    get_jwt, verify_jwt_in_request
)
from sqlalchemy.exc import IntegrityError


auth_bp = Blueprint("auth", __name__)


# ---------------- Landing page ----------------
@jwt_required(optional=True)
@auth_bp.get("/")
def landing_page():
    try:
        identity=get_jwt_identity()
        if identity:
            return redirect(url_for("home.home"), user_name=identity["name"])
    except Exception:
        pass
    # No token -> show landing page
    return render_template("landing_page.html")


# ---------------- Google OAuth ----------------
@auth_bp.get("/google_login")
def google_login():
    return oauth.Infoledge.authorize_redirect(redirect_url=url_for("auth.google_signin", _external=True))


@auth_bp.get("/google_signin")
def google_signin():
    try:
        token = oauth.Infoledge.authorize_access_token()
        user_info = oauth.Infoledge.parse_id_token(token)
        
        session["user"] = {
            "provider": "google",
            "email": user_info.get("email"),
            "name": user_info.get("name"),
            "access_token": token.get("access_token")
        }
        # JWT token
        access_token = create_access_token(
            identity=user_info.get("email"),  # must be string/int
            additional_claims={"id": user_info.get("id"), "name": user_info.get("name")}
        )
        refresh_token = create_refresh_token(
            identity=user_info.get("email"),
            additional_claims={"id": user_info.get("id"), "name": user_info.get("name")}
        )
        
        user_name = user_info.get("name", None)
        resp = redirect(url_for('home.home', user_name=user_name))
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp
    except:
        return redirect(url_for('auth.landing_page'))
    
        

# ---------------- Local Auth (SQL + JWT) ----------------
@auth_bp.get('/profile')
@auth_bp.get('/debug')
def profile():
    try:
        verify_jwt_in_request()  # will raise exception if token invalid
        identity = get_jwt_identity()
        claims = get_jwt()
        return jsonify({"identity": identity, "claims": claims})
    except Exception as e:
        return jsonify({"error": str(e)}), 401

# Register/Sign UP
@auth_bp.post("/register")
def register():
    data = request.get_json(silent=True)
    email = data.get("email").lower().strip()
    password = data.get("password")
    name = data.get("name")
    
    if not email and not password:
        return jsonify({"error": "Email and Password required"}), 400
    if not email:
        return jsonify({"error": "Email is missing"}), 400
    if not password:
        return jsonify({"error": "Password is missing"}), 400
    if not re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email):
        return jsonify({"error": "Please provide a valid email address"}), 400
    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters long."}), 400
    
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify({"error": "Email already exists...Try Logging in"}), 409
    
    user = User.create(email=email, name=name, password=password)
    db.session.add(user)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": e}), 409
    
    # issue tokens so the user is logged in immediately
    identity = user.email
    additional_claims = {"id": user.id, "name": user.name}
    access_token = create_access_token(
        identity=identity,  # must be string/int
        additional_claims=additional_claims
    )
    refresh_token = create_refresh_token(
        identity=identity,
        additional_claims=additional_claims
    )
    
    resp = jsonify({"message": "User registered successfully", "redirect": url_for('home.home', user_name=user.name)})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp, 201

# Login
@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True)
    email = data.get("email").lower().strip()
    password = data.get("password")
    
    if not email and not password:
        return jsonify({"error": "Email and Password required"}), 400
    if not email:
        return jsonify({"error": "Email is missing"}), 400
    if not password:
        return jsonify({"error": "Password is missing"}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if (not user) or (not user.check_password(password)):
        return jsonify({"error": "Invalid credentials"}), 401
    #  Create tokens
    identity = user.email
    additional_claims = {"id": user.id, "name": user.name}
    access_token = create_access_token(
        identity=identity,  # must be string/int
        additional_claims=additional_claims
    )
    refresh_token = create_refresh_token(
        identity=identity,
        additional_claims=additional_claims
    )
    # Send tokens in cookies
    resp = jsonify({"message": "Login Successful", "redirect": url_for('home.home', user_name=user.name)})
    set_access_cookies(resp, access_token)
    set_refresh_cookies(resp, refresh_token)
    return resp, 200

#  Refresh
@auth_bp.post("/refresh")
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    claims = get_jwt()
    additional_claims = {"id": claims["id"], "name": claims["name"]}
    access_token = create_access_token(identity=identity, additional_claims=additional_claims)
    resp = jsonify({"message": "token refreshed"})
    set_access_cookies(resp, access_token)
    return resp, 200


# ---------------- Logout (Google + JWT) ----------------
@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    user = session.get("user", None)
    
    if user and user.get("provider") == "google":
        token = user.get("access_token")
        if token:
            try:
                requests.post('https://oauth2.googleapis.com/revoke', params={'token': token})
            except Exception as e:
                flash(f"Google revoke failed {e}")
        session.clear()
    
    resp = redirect(url_for('auth.landing_page'))
    unset_jwt_cookies(resp)
    return resp
