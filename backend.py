from flask import Flask, render_template
import firebase_admin
import os
from firebase_admin import credentials
from google.cloud import firestore
import json

#cred = credentials.Certificate("config/firebasesecrets.json")
#firebase_admin.initialize_app(cred)
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'config/firebasesecrets.json'

app = Flask(__name__)
db = firestore.Client()

@app.route('/')
def home():
    return render_template('homepage.html', shelters=getAllShelters())

@app.route('/signup')
def signup():
    return render_template('signuppage.html')

@app.route('/login')
def login():
    return render_template('loginpage.html')

@app.route('/account')
def account():
    return render_template('account.html', shelters=getAllShelters())


def getAllShelters():
    shelters = []
    # Then query for documents
    shelters_ref = db.collection(u'shelters')
    shelter_docs = shelters_ref.get()
    for shelter in shelter_docs:
        shelters.append(shelter.to_dict())
        print(str(type(shelter.to_dict())))

    return shelters
