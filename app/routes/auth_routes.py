from flask import Blueprint, session, render_template, redirect, url_for, request, flash
import requests
from app import oauth


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def landing_page():
    if session.get("user"):
        return redirect(url_for('home.home'))
    return render_template("landing_page.html")


@auth_bp.route("/google-login")
def google_login():
    return oauth.Infoledge.authorize_redirect(redirect_url=url_for("auth.google_signin", external=True))


@auth_bp.route("/google-signin")
def google_signin():
    try:
        token = oauth.Infoledge.authorize_access_token()
        session['user'] = token
        return redirect(url_for('home.home'))
    except:
        return redirect(url_for('auth.landing_page'))


@auth_bp.route('/logout', methods=["POST"])
def logout():
    if session.get("user"):
        token = session['user'].get("access_token")
        requests.post('https://oauth2.googleapis.com/revoke', params={'token': token})
    session.clear()
    return redirect(url_for('auth.landing_page'))
    
