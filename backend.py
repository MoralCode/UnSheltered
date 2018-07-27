from flask import Flask, render_template
import json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html', shelters=get_shelter_list())

@app.route('/signup')
def signup():
    return render_template('signuppage.html')



def get_shelter_list():
    return [{
        "name": "Awesome Minds Homeless Shelter",
        "bedsFree": 62
    },
    {
        "name": "Healthy Happy Habitat",
        "bedsFree": 23
    }]