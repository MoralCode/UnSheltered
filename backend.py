from flask import Flask
from flask import redirect
from flask import request
from flask import render_template
from flask import session
from flask import url_for
import os
# from google.cloud import firestore
from pymongo import MongoClient
from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode 
# from classes.Shelter import Shelter
#CONSTANTS
JWT_PAYLOAD = 'jwt_payload'
PROFILE_KEY = 'profile'


client = MongoClient(os.environ.get('DATABASE_URL'))
db = client.unsheltereddb

app = Flask(__name__)
oauth = OAuth(app)
# db = firestore.Client()
# shelters_ref = db.collection(u'shelters')



app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']
base_url='https://' + 'unsheltered.auth0.com'
AUTH0_AUDIENCE = base_url + '/userinfo'

auth0 = oauth.register(
    'auth0',
    client_id = os.environ['AUTH0_CLIENT_ID'],
    client_secret = os.environ['AUTH0_CLIENT_SECRET'],
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

def getCurrentUserId():
    return session[PROFILE_KEY]['user_id']


def processShelterEdit(shelter, delete=False):
    if shelter['id'] == '':
        addShelter(shelter)
    elif delete:
        deleteShelter(shelter)
    else:
        updateShelter(shelter)

@app.context_processor
def injectLoginState():
    return dict(loggedin=isLoggedIn())

# def requires_auth(f):
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         if not isLoggedIn():
#             return redirect('/account')
#         return f(*args, **kwargs)

#     return decorated


@app.route('/')
def home():
    return render_template('homepage.html', shelters=getShelters())


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

@app.route('/volunteer')
def volunteer():
    return render_template('volunteer.html') 

@app.route('/homelessRights')
def homelessRights():
    return render_template('homelessRights.html')  

@app.route('/about')
def about():
    return render_template('about.html')  

@app.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'GET':
        if isLoggedIn():
            return render_template(
                'account.html',
                shelters=getShelters({'owner': str(getCurrentUserId())})
                )
            # userinfo=session[PROFILE_KEY], #these are ost likely unnecessary
            # userinfo_pretty=json.dumps(session[JWT_PAYLOAD], indent=4)
        else:
            return auth0.authorize_redirect(
                redirect_uri=url_for('callbackHandling', _external=True),
                audience=AUTH0_AUDIENCE
                )
    elif request.method == 'POST':
        form = request.form

        shelter = {
            'name': form.getlist('shelter-name')[0],
            'id': form.getlist('shelter-id')[0],#for checking if its a new shelter or editing one
            'owner': str(getCurrentUserId()),
            'capacity': int(form.getlist('shelter-capacity')[0]),
            'bedsFree': int(form.getlist('available-beds')[0])
        }
        try:
            shouldDelete = form.getlist('deletion-checkbox')[0] == 'true'
        except IndexError:
            shouldDelete = False

        processShelterEdit(shelter, shouldDelete)
        return redirect('/account')

@app.route('/logout')
def logout():
    session.clear()
    params = {
        'returnTo': url_for('home', _external=True),
        'client_id': os.environ['AUTH0_CLIENT_ID']
        }
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


def getShelters(query=None):
    allShelters = []
    if query is None:
        shelters = db.shelters.find()
    else:
        shelters = db.shelters.find(query)
        print(query)

    for shelter in shelters:
        print(shelter)
        allShelters.append(shelter)

    print(allShelters)
    return allShelters


def addShelter(shelter):
    db.shelters.insert(shelter)

def deleteShelter(shelter):
    return

def updateShelter(shelter):
    return
