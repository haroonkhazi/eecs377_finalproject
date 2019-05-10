from flask import Flask, render_template, request, redirect, jsonify, session, url_for
from flask import Markup, send_file
from six.moves.urllib.parse import urlencode
from werkzeug.exceptions import HTTPException
import os
from authlib.flask.client import OAuth
from os import walk
from functools import wraps
from os import environ as env
from dotenv import load_dotenv, find_dotenv
from os.path import join, dirname, realpath
import constants
#from StringIO import StringIO

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)



AUTH0_CALLBACK_URL = env.get(constants.AUTH0_CALLBACK_URL)
AUTH0_CLIENT_ID = env.get(constants.AUTH0_CLIENT_ID)
AUTH0_CLIENT_SECRET = env.get(constants.AUTH0_CLIENT_SECRET)
AUTH0_DOMAIN = env.get(constants.AUTH0_DOMAIN)
AUTH0_BASE_URL = 'https://' + AUTH0_DOMAIN
AUTH0_AUDIENCE = env.get(constants.AUTH0_AUDIENCE)
if AUTH0_AUDIENCE is '':
    AUTH0_AUDIENCE = AUTH0_BASE_URL + '/userinfo'

app = Flask(__name__, static_url_path='/static', static_folder='./templates/static')
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=AUTH0_CLIENT_ID,
    client_secret=AUTH0_CLIENT_SECRET,
    api_base_url=AUTH0_BASE_URL,
    access_token_url=AUTH0_BASE_URL + '/oauth/token',
    authorize_url=AUTH0_BASE_URL + '/authorize',
    client_kwargs={
        'scope': 'openid profile',
    },
)


app.secret_key = constants.SECRET_KEY
app.debug = True


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if constants.PROFILE_KEY not in session:
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated

@app.errorhandler(Exception)
def handle_auth_error(ex):
    response = jsonify(message=str(ex))
    response.status_code = (ex.code if isinstance(ex, HTTPException) else 500)
    return response

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=AUTH0_CALLBACK_URL, audience=AUTH0_AUDIENCE)

@app.route('/callback')
def callback_handling():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()
    session[constants.JWT_PAYLOAD] = userinfo
    session[constants.PROFILE_KEY] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/')


@app.route('/')
@requires_auth
def home():
    imagepath = "/Users/haroonkhazi/Desktop/EECS377/final_project/website/templates/static/"
    files =[]
    for (dirpath, dirnames, filenames) in walk(imagepath):
        files.extend(filenames)
        break
    files = [f for f in files if "picture" in f]
    files.sort()
    return render_template('home.html', files=files)

@app.route('/videos')
@requires_auth
def done():
    imagepath = "/Users/haroonkhazi/Desktop/EECS377/final_project/website/templates/static/"
    files = []
    for (dirpath, dirnames, filenames) in walk(imagepath):
        files.extend(filenames)
        break
    files = [f for f in files if "mp4" in f]
    files.sort()
    print(files)
    return render_template('video.html', files=files)

@app.route('/static/<pngFile>.png')
@requires_auth
def serve_image(pngFile):
    return send_file('/Users/haroonkhazi/Desktop/EECS377/final_project/website/templates/static/'+pngFile+'.png')

@app.route('/static/<svgFile>.svg')
def serve_content(svgFile):
    return send_file('/Users/haroonkhazi/Desktop/EECS377/final_project/website/templates/static/'+svgFile+'.svg', mimetype='image/svg+xml')

@app.route('/logout')
def logout():
    session.clear()
    params = {'returnTo': url_for('home', _external=True), 'client_id': AUTH0_CLIENT_ID}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='5000')
