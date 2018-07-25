from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('homepage.html', test="Hello")

@app.route('/signup')
def hello():
    return render_template('signuppage.html')