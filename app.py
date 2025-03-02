import os
import requests
import urllib.parse
from dotenv import load_dotenv
from datetime import datetime, timedelta
from flask import Flask, render_template, url_for, redirect, request, session, flash, jsonify
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
spotifyConfig = {
    "SPOTIFY_CLIENT_ID": os.getenv("SPOTIFY_CLIENT_ID"),
    "SPOTIFY_SECRET_KEY": os.getenv("SPOTIFY_SECRET_KEY"),
    "SPOTIFY_AUTH_URL": os.getenv("SPOTIFY_AUTH_URL"),
    "SPOTIFY_TOKEN_URL": os.getenv("SPOTIFY_TOKEN_URL"),
    "SPOTIFY_API_BASE_URL": os.getenv("SPOTIFY_API_BASE_URL")
}
print(spotifyConfig)

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
                   "scope" : "openid profile email https://www.googleapis.com/auth/user.birthday.read",
               }
               )


@app.before_request
def make_session_permanent():
    if session.get("user"):
        session.permanent = True

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

#----Home page----
@app.route('/home', methods=['GET', 'POST'])
def home():
    if request.method=='GET':
        if session.get("user"):
            return render_template('home.html')
        else:
            flash('Sign in required !')
            return redirect(url_for('googleLogin'))
    # if request.method=='POST':
    #     action = request.form.get('action')
    

#------Spotify-------


@app.route('/spotifyLogin', methods=['POST'])
def spotifyLogin():
    #  pass these params to spotify to get spotify's authorization. Spotify will return me it's auth code.
    
    scope = 'user-read-private user-read-email'
    params = {
        'client_id': spotifyConfig.get("SPOTIFY_CLIENT_ID"),
        'response_type': 'code',    # This is the auth code, which'll be later used to to exchange access token.
        'scope': scope,             # These are the permissions I need from spotify to access from users
        'redirect_uri': url_for('spotifyCallback', _external=True), # URL where Spotify will send the user after they login
        'show_dialog': True        # True- Spotify will force the user to log in every time, even if previously logged in
    }
    auth_url = f'{spotifyConfig.get("SPOTIFY_AUTH_URL")}?{urllib.parse.urlencode(params)}'
    return redirect(auth_url)       # Send the user to spotify's login page

    
# The route user will be redirected to after logging in with spotify
@app.route('/spotifyCallback')
def spotifyCallback():
    if 'error' in request.args:
        error_message = jsonify({"error": request.args.get("error")})
        flash('There was an error while login...Try again\n')
        return redirect(url_for('home'))
    if 'code' in request.args:
        req_body = {
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': url_for('spotifyCallback', _external=True),
            'client_id': spotifyConfig.get("SPOTIFY_CLIENT_ID"),
            'client_secret': spotifyConfig.get("SPOTIFY_SECRET_KEY")
        }
        response = requests.post(spotifyConfig.get("SPOTIFY_TOKEN_URL"), data=req_body)
        spotify_token = response.json()
        session['access_token'] = spotify_token.get('access_token')
        session['refresh_token'] = spotify_token.get('refresh_token')
        expires_in = spotify_token.get('expires_in')
        session['expires_at'] = datetime.now().timestamp() + expires_in

        return redirect('/playlists')

@app.route('/playlists')
def playlists():
    if 'access_token' not in session:
        return redirect(url_for('spotifyLogin'))
    
    if datetime.now().timestamp() > session.get('expires_at'):
        print('Session Expired')
        return redirect(url_for('refreshToken'))
    
    # Else we can get user's spotify account details
    headers = {
        'Authorization': f"Bearer {session['access_token']}",
    }
    response = requests.get(spotifyConfig.get("SPOTIFY_API_BASE_URL") + 'me/playlists', headers=headers)
    playlists = response.json()
    
    return jsonify(playlists)


# Refresh tokens
@app.route('/refreshToken')
def refreshToken():
    if 'refresh_token' not in session:
        redirect(url_for('spotifyLogin'))
    if datetime.now().timestamp() > session.get('expires_at'):
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session.get('refresh_token'),
            'client_id': spotifyConfig.get("SPOTIFY_CLIENT_ID"),
            'client_secret': spotifyConfig.get("SPOTIFY_SECRET_KEY")
        }
        response = requests.post(spotifyConfig.get("SPOTIFY_TOKEN_URL"), data=req_body)
        new_spotify_token = response.json()
        
        session['access_token'] = new_spotify_token['access_token']
        expires_in = new_spotify_token['expires_in']
        session['expires_at'] = datetime.now().timestamp() + expires_in

        return redirect('/playlists')


if __name__ == '__main__':
    app.run(host="localhost", port=flaskConfig.get("FLASK_PORT"), debug=True)
    