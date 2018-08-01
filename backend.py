from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
import firebase_admin
from functools import wraps
from os import environ
from werkzeug.exceptions import HTTPException
from firebase_admin import credentials
from google.cloud import firestore
import json
from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode
from dotenv import load_dotenv, find_dotenv

#CONSTANTS
JWT_PAYLOAD = 'jwt_payload'
PROFILE_KEY = 'profile'


app = Flask(__name__)
oauth = OAuth(app)
db = firestore.Client()

app.config['SECRET_KEY'] = environ['FLASK_SECRET_KEY']
base_url='https://' + 'unsheltered.auth0.com'
AUTH0_AUDIENCE = base_url + '/userinfo'

auth0 = oauth.register(
    'auth0',
    client_id = environ['AUTH0_CLIENT_ID'],
    client_secret = environ['AUTH0_CLIENT_SECRET'],
    api_base_url = base_url,
    access_token_url = base_url + '/oauth/token',
    authorize_url = base_url + '/authorize',
    client_kwargs = {
        'scope': 'openid profile',
    },
)

def isLoggedIn():
    # print('trolololol')
    # print('profile' in session)
    # print(session)
    return ('profile' in session)

@app.context_processor
def injectLoginState():
    return dict(loggedin=isLoggedIn())

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not isLoggedIn():
            return redirect('/login')
        return f(*args, **kwargs)

    return decorated


@app.route('/')
def home():
    return render_template('homepage.html', shelters=getAllShelters())

@app.route('/signup')
def signup():
    return render_template('signuppage.html')

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=url_for('callbackHandling', _external=True), audience=AUTH0_AUDIENCE)

@app.route('/logincallback')
def callbackHandling():
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    session[JWT_PAYLOAD] = userinfo
    session[PROFILE_KEY] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/account')

@app.route('/account')
@requires_auth
def account():
    return render_template(
        'account.html',
        userinfo=session[PROFILE_KEY],
        userinfo_pretty=json.dumps(session[JWT_PAYLOAD], indent=4)
    )


@app.route('/logout')
def logout():
    session.clear()
    params = {
        'returnTo': url_for('home', _external=True),
        'client_id': AUTH0_CLIENT_ID
        }
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


def getAllShelters():
    shelters = []
    # Then query for documents
    shelters_ref = db.collection(u'shelters')
    shelter_docs = shelters_ref.get()
    for shelter in shelter_docs:
        shelterEntry = shelter.to_dict()
        shelterEntry['id'] = shelter.id
        shelters.append(shelterEntry)
    return shelters
