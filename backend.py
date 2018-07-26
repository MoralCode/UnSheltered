from flask import Flask, render_template
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("config/firebasesecrets.json")
firebase_admin.initialize_app(cred)

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html', test="Hello")

@app.route('/signup')
def signup():
    return render_template('signuppage.html')