from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('homepage.html', test="Hello")

@app.route('/signup')
def signup():
    return render_template('signuppage.html')