from flask import Flask
from flask import redirect
from flask import request
from flask import render_template
from flask import session
from flask import url_for
from flask import flash
import os
import json
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
gmaps = googlemaps.Client(key=os.environ.get('MAPS_APIKEY'))


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
    flash('You were successfully logged in', 'alert-success')
    return redirect('/account')

@app.route('/volunteer')
def volunteer():
    return render_template('volunteer.html') 

@app.route('/homelessrights')
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

        if formData['bedsFree'] > formData['capacity']:
            flash('Error: The number of beds available cannot be higher than the shelter capacity.', 'alert-danger')
            return redirect('/account')

        if getNearestPlaceWithName(constructAddress(formData), formData['name']) == None:
            flash('Error: The address you provided could not be found in the Google Maps database.', 'alert-danger')
            return redirect('/account')

        for field in form:
            if field == 'delete':
                print("deleting")
                deleteShelter(ObjectId(str(form.getlist('shelter-id')[0])))
                break

            elif field == 'update':
                print("updating")
                formData['_id'] = ObjectId(str(form.getlist('shelter-id')[0]))
                updateShelter(formData)
                break
                
            elif field == 'submit':
                print("creating")
                addShelter(formData)
                break
                
        return redirect('/account')

@app.route('/logout')
def logout():
    session.clear()
    params = {
        'returnTo': url_for('home', _external=True),
        'client_id': os.environ['AUTH0_CLIENT_ID']
        }
    flash('You were successfully logged out', 'alert-success')
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


def getShelters(query=None):
    allShelters = []
    if query is None:
        shelters = db.shelters.find()
    else:
        shelters = db.shelters.find(query)

    for shelter in shelters:
        
        shelter["mapURL"] = getMapURLForShelter(constructAddress(shelter), shelter['name'])
        allShelters.append(shelter)

    return allShelters


def addShelter(shelter):
    db.shelters.insert(shelter)
    flash('Shelter Added!', 'alert-success')

def deleteShelter(id):
    db.shelters.delete_one({ "_id": id })
    flash('Shelter Deleted!', 'alert-success')

def updateShelter(shelterData):
    shelterQuery={ '_id': shelterData['_id']}
    shelter=getShelters({ '_id': shelterData['_id']})[0]
    updateQuery={}

    for key, value in shelterData.items():
        if shelter[key] != value: 
            updateQuery[key] = value


    if updateQuery == {}:
        flash("Could not update this shelter. No information has changed", 'alert-danger')
        return

    updateQuery = { "$set": updateQuery }
  
    db.shelters.update_one(shelterQuery, updateQuery)
    flash('Shelter Updated!', 'alert-success')

def getURL(address):
    geocode_result = gmaps.geocode(address)#111 W Burnside St, Portland, OR
    #print(json.dumps(geocode_result, indent=4, sort_keys=True))
    lat=str(float(geocode_result[0]["geometry"]["location"]["lat"]))
    lng=str(float(geocode_result[0]["geometry"]["location"]["lng"]))
    placeid=(geocode_result[0]["place_id"])
    url_string = "https://www.google.com/maps/search/?api=1&query="+lat+","+lng+"&query_place_id="+placeid
    return (url_string)
    #((geocode_result[0]["geometry"]["location"]["lat"]), (geocode_result[0]["geometry"]["location"]["lng"])) 
    
def getAddressPlace(address):
    geocode_result = gmaps.geocode(address)#111 W Burnside St, Portland, OR
    return geocode_result[0]["place_id"]
    #((geocode_result[0]["geometry"]["location"]["lat"]), (geocode_result[0]["geometry"]["location"]["lng"])) 
    
def constructAddress(shelterDict):
    return shelterDict["streetAddress"]+", "+shelterDict["city"]+", "+shelterDict["state"]+" "+shelterDict["zipcode"]

def getLatLong(address):
    geocode_result = gmaps.geocode(address)#111 W Burnside St, Portland, OR
    #print(json.dumps(geocode_result, indent=4, sort_keys=True))
    lat=float(geocode_result[0]["geometry"]["location"]["lat"])
    lng=float(geocode_result[0]["geometry"]["location"]["lng"])
    return (lat, lng)

def getPlaceIdFromAddress(address):
    places = gmaps.find_place(input=[address], input_type='textquery', fields=['place_id'])
    # input (list) – The text input specifying which place to search for (for example, a name, address, or phone number).
    # input_type (string) – The type of input. This can be one of either ‘textquery’ or ‘phonenumber’.
    # fields – The fields specifying the types of place data to return, separated by a comma. For full details see: https://developers.google.com/places/web-service/search#FindPlaceRequests
    # location_bias (string) – Prefer results in a specified area, by specifying either a radius plus lat/lng, or two lat/lng pairs representing the points of a rectangle. See: https://developers.google.com/places/web-service/search#FindPlaceRequests
    # language – The language in which to return results.
    # https://googlemaps.github.io/google-maps-services-python/docs/#googlemaps.Client.find_place
    return places['candidates'][0]['place_id']

def getNearestPlaceWithName(address, name):
    coords = getLatLong(address)
    places=gmaps.places_nearby(coords, keyword=name, rank_by='distance')#, type="lodging"
    #     location (string, dict, list, or tuple) – The latitude/longitude value for which you wish to obtain the closest, human-readable address.
    #     radius (int) – Distance in meters within which to bias results.
    #     region (string) – The region code, optional parameter. See more @ https://developers.google.com/places/web-service/search
    #     keyword (string) – A term to be matched against all content that Google has indexed for this place.
    #     language – The language in which to return results.
    #     min_price (int) – Restricts results to only those places with no less than this price level. Valid values are in the range from 0 (most affordable) to 4 (most expensive).
    #     max_price (int) – Restricts results to only those places with no greater than this price level. Valid values are in the range from 0 (most affordable) to 4 (most expensive).
    #     name (string or list of strings) – One or more terms to be matched against the names of places.
    #     open_now (bool) – Return only those places that are open for business at the time the query is sent.
    #     rank_by (string) – Specifies the order in which results are listed. Possible values are: prominence (default), distance
    #     type (string) – Restricts the results to places matching the specified type. The full list of supported types is available here: https://developers.google.com/places/supported_types
    #     page_token (string) – Token from a previous search that when provided will returns the next page of results for the same search.

    # Return type:	

    # result dict with the following keys: status: status code results: list of places html_attributions: set of attributions which must be displayed next_page_token: token for retrieving the next page of results

    try:
        placeID=places['results'][0]['place_id']
    except IndexError:
        return None
    else:
        return placeID

def getUrlFromPlaceID(placeID):
    return "https://www.google.com/maps/place/?q=place_id:" + str(placeID)

def getMapURLForShelter(address, name):
    placeID = getNearestPlaceWithName(address, name)
    print(type(placeID))
    if placeID == None:
        placeID = getAddressPlace(address)
    
    return getUrlFromPlaceID(placeID)
    


# print(getUrlFromPlaceID(getNearestPlaceWithName('22 SW 3rd Ave, Portland, OR 97204', 'Voodoo Doughnut')))