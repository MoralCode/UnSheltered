from flask import Flask
from flask import redirect
from flask import request
from flask import render_template
from flask import session
from flask import url_for
from flask import flash
import os
import json
# from google.cloud import firestore
from pymongo import MongoClient
from bson.objectid import ObjectId
from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode 
import googlemaps
from datetime import datetime

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
    if not hasattr(shelter, '_id'):
        addShelter(shelter)
    elif delete:
        deleteShelter(shelter['_id'])
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
    flash('You were successfully logged in')
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
        formData = {
            'name': form.getlist('name')[0],
            'owner': str(getCurrentUserId()),#potential security issue?
            'capacity': int(form.getlist('capacity')[0]),
            'bedsFree': int(form.getlist('bedsFree')[0]),
            'streetAddress': form.getlist('streetaddress')[0],
            'city': 'Portland',
            'state': 'Oregon',
            'zipcode': form.getlist('zipcode')[0]
        }
        if (str(form.getlist('shelter-id')[0]) != ''):
            formData['_id'] = ObjectId(str(form.getlist('shelter-id')[0]))

        if hasattr(form, 'delete'):
            processShelterEdit(formData, True)
        elif hasattr(form, 'update'):
            processShelterEdit(formData, False)

        return redirect('/account')

@app.route('/logout')
def logout():
    session.clear()
    params = {
        'returnTo': url_for('home', _external=True),
        'client_id': os.environ['AUTH0_CLIENT_ID']
        }
    flash('You were successfully logged out')
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


def getShelters(query=None):
    allShelters = []
    if query is None:
        shelters = db.shelters.find()
    else:
        shelters = db.shelters.find(query)

    for shelter in shelters:
        shelter["mapURL"] = getURL(shelter["streetAddress"]+", "+shelter["city"]+", "+shelter["state"]+" "+shelter["zipcode"])
        allShelters.append(shelter)

    return allShelters


def addShelter(shelter):
    db.shelters.insert(shelter)
    flash('Shelter Added!')

def deleteShelter(id):
    db.shelters.delete_one({ "_id": id })
    flash('Shelter Deleted!')

def updateShelter(shelterData):
    shelterQuery={ '_id': shelterData['_id']}
    shelter=getShelters({ '_id': shelterData['_id']})[0]
    updateQuery=None

    for key, value in shelterData.items():
        if shelter[key] != value: 
            updateQuery[key] = value


    if updateQuery is None:
        # flash
        return

    updateQuery = { "$set": updateQuery }
  
    db.shelters.update_one(shelterQuery, updateQuery)
    flash('Shelter Updated!')

def getURL(address):
    gmaps = googlemaps.Client(key=os.environ.get('MAPS_APIKEY'))
    geocode_result = gmaps.geocode(address)#111 W Burnside St, Portland, OR
    #print(json.dumps(geocode_result, indent=4, sort_keys=True))
    lat=str(float(geocode_result[0]["geometry"]["location"]["lat"]))
    lng=str(float(geocode_result[0]["geometry"]["location"]["lng"]))
    placeid=(geocode_result[0]["place_id"])
    url_string = "https://www.google.com/maps/search/?api=1&query="+lat+","+lng+"&query_place_id="+placeid
    return (url_string)
    #((geocode_result[0]["geometry"]["location"]["lat"]), (geocode_result[0]["geometry"]["location"]["lng"])) 
    getURL("111 W Burnside St, Portland, OR")
