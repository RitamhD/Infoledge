import os
import requests
from functools import wraps
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flask import Flask, render_template, url_for, redirect, request, session, flash
from authlib.integrations.flask_client import OAuth
# import mysql.connector

load_dotenv()
flaskConfig = {
    "FLASK_SECRET_KEY": os.getenv("FLASK_SECRET_KEY"),
    "FLASK_PORT": os.getenv("FLASK_PORT") 
}
oauthConfig = {
    "OAUTH_CLIENT_ID": os.getenv("OAUTH_CLIENT_ID"),
    "OAUTH_CLIENT_SECRET_KEY": os.getenv("OAUTH_CLIENT_SECRET_KEY"),
    "OAUTH_META_URL": os.getenv("OAUTH_META_URL"),
}
# youtubeConfig = {
#     "YOUTUBE_API_KEY": os.getenv("YOUTUBE_API_KEY"),
#     "YOUTUBE_SEARCH_URL": os.getenv("YOUTUBE_SEARCH_URL"),
#     "YOUTUBE_VIDEO_URL": os.getenv("YOUTUBE_VIDEO_URL"),
# }


# #----Backend----
app = Flask(__name__, template_folder='view', static_folder='static')

app.config['SECRET_KEY'] = flaskConfig.get("FLASK_SECRET_KEY")
app.config['SESSION_PERMANENT'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

oauth = OAuth(app)
oauth.register("Infoledge",
               client_id = oauthConfig.get("OAUTH_CLIENT_ID"),
               client_secret = oauthConfig.get("OAUTH_CLIENT_SECRET_KEY"),
               server_metadata_url = oauthConfig.get("OAUTH_META_URL"),
               client_kwargs = {
                   "scope" : "openid profile email",
               }
               )


# @app.before_request
# def make_session_permanent():
#     if session.get("user"):
#         session.permanent = True

#----Landing page----
@app.route('/', methods=['GET', 'POST'])
def landing_page():
    if request.method=='GET':
        if session.get("user"):
            return redirect(url_for('home'))
        else:
            return render_template('landing_page.html')
    elif request.method=='POST':
        return redirect(url_for('googleLogin'))    

#----Google Sign in----
@app.route('/google-login')
def googleLogin():
    return oauth.Infoledge.authorize_redirect(redirect_uri=url_for('googleSignin', _external=True))

@app.route('/signin-google')
def googleSignin():
    try:
        token = oauth.Infoledge.authorize_access_token()
        session["user"] = token
        return redirect(url_for('home'))
    except:
        return redirect(url_for('landing_page'))
    
#----Logout----
def revoke_google_token(token):
    revoke_url = 'https://oauth2.googleapis.com/revoke'
    params = {'token': token}
    response = requests.post(revoke_url, params=params)
    return response.status_code==200

@app.route('/logout', methods=['POST'])
def logout():
    if session.get("user"):
        token = session["user"].get("access_token")
        revoke_google_token(token)
    session.clear()
    return redirect(url_for('landing_page'))



#----Login----
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("user"):  # Check if user exists in session
            flash('Sign in required!')
            return redirect(url_for('googleLogin'))  # Redirect to login page if not logged in
        return f(*args, **kwargs)  # If logged in, continue with the route function
    return decorated_function


#----Home page----
@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    if request.method=='GET':
        return render_template('home.html')
        
    if request.method=='POST':
        action = request.form.get('action')
        if action == "codemirror":
            return redirect(url_for('code_platform'))
        



#-----Code Platform-----
@app.route('/code_platform')
@login_required
def code_platform():
    return render_template('code_platform.html')



if __name__ == '__main__':
    app.run()
    