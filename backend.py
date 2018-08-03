from flask import Flask
# from flask import redirect
from flask import request
from flask import render_template
from flask import session
from flask import url_for
from os import environ
from google.cloud import firestore
from authlib.flask.client import OAuth
from classes.Shelter import Shelter

#CONSTANTS
JWT_PAYLOAD = 'jwt_payload'
PROFILE_KEY = 'profile'


app = Flask(__name__)
oauth = OAuth(app)
db = firestore.Client()
shelters_ref = db.collection(u'shelters')

if environ['GOOGLE_APPLICATION_CREDENTIALS'] is None:
    environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'config/firebasesecrets.json'

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

def getCurrentUserId():
    return session[PROFILE_KEY]['user_id']


def processShelterEdit(shelter, delete=False):
    if shelter.id == '':
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
    return render_template('homepage.html', shelters=getAllShelters())


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
                shelters=getSheltersOwnedByCurrentUser()
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

        bedsOccupied = int(form.getlist('shelter-capacity')[0]) - int(form.getlist('available-beds')[0])

        shelter = Shelter(
            form.getlist('shelter-name')[0],
            form.getlist('shelter-id')[0],
            str(getCurrentUserId()),
            int(form.getlist('shelter-capacity')[0]),
            bedsOccupied
        )
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
        'client_id': environ['AUTH0_CLIENT_ID']
        }
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


def getAllShelters():
    shelters = []
    # Then query for documents
    shelter_docs = shelters_ref.get()
    for shelter in shelter_docs:
        shelterEntry = shelter.to_dict()
        shelters.append(
            Shelter(
                shelterEntry['name'],
                shelter.id,
                shelterEntry['ownedby'],
                shelterEntry['capacity'],
                shelterEntry['bedsoccupied']
                )
            )
        # shelters.append(shelterEntry)
    return shelters

def getSheltersOwnedByCurrentUser():
    allShelters = getAllShelters()
    userShelters = []

    for shelter in allShelters:
        if (shelter.owner == getCurrentUserId()):
            userShelters.append(shelter)
    return userShelters

def addShelter(shelter):
    newShelter = Shelter(
        shelter.name,
        None,
        getCurrentUserId(),
        shelter.capacity,
        shelter.bedsOccupied
    )
    shelters_ref.add(newShelter.to_dict())
    return


def deleteShelter(shelter):
    shelters_ref.document(shelter.id).delete()
    #Warning: Deleting a document does not delete its subcollections!
    #When you delete a document that has associated subcollections, the subcollections are not deleted. They are still accessible by reference. For example, there may be a document referenced by db.collection('coll').doc('doc').collection('subcoll').doc('subdoc') even though the document referenced by db.collection('coll').doc('doc') no longer exists. If you want to delete documents in subcollections when deleting a document, you must do so manually, as shown in Delete Collections below.
    return

def updateShelter(shelter):
    # Add a new doc in collection 'cities' with ID 'LA'
    # shelters_ref.document(u'LA').set(data)

    # The option to merge data is not yet available for Python. Instead, call the
    # update method and pass the option to create the document if it's missing.
    shelters_ref.document(shelter.id).update(
        shelter.to_dict(),
        firestore.CreateIfMissingOption(True)
        )
    return