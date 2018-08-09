**Note:** The forms on this site are known to be vulnerable to CSRF (Cross-Site Request Forgery). 
![Homepage of UnSheltered](homepagescreenshot.png)
# UnSheltered
 An online listing and occupancy tracking system for homeless shelters. The homelessness crisis in Portland continues to increase with 57% being unsheltered. The goal of our website is to allow the local homeless to find shelters with enough spaces and that has needed amenities. In addition, our app educates homeless youth on their educational rights as well as advertising volunteer opportunities for local community members or homeless that want to give back to shelters.




## Setup
You will need [Python 3.x](https://www.python.org/downloads/) installed to use this app. Python 2 is not tested at all. You have been warned.

1. make sure you run `pip install pipenv` or `python -m pip install pipenv` to install `pipenv`
> If pipenv isn’t available in your shell after installation, you’ll need to add the user base’s binary directory to your PATH.

https://docs.pipenv.org/install/#installing-pipenv

3. run `pipenv sync`

The project and all its dependencies should now be correctly set up. Windows may have some issues as we experienced.


## Run 
[Source](https://github.com/pallets/flask)


1. Run `pipenv shell` to enter the environment created by pipenv.
2. Set environment variables. You will need to do these every time you restart flask so it may be advisable to make a script for this. Refer to the table below for what you should set

Variable Name | Value
------------ | -------------
FLASK_APP | The name of the main python file. `backend.py` in this case. [More](http://flask.pocoo.org/docs/1.0/tutorial/factory/#run-the-application) [Info](http://flask.pocoo.org/docs/1.0/config/#environment-and-debug-features)
FLASK_ENV | Set this to `development` if you want to have flask auto-update changed files without having to restart manually. [More](http://flask.pocoo.org/docs/1.0/tutorial/factory/#run-the-application) [Info](http://flask.pocoo.org/docs/1.0/config/#environment-and-debug-features)
AUTH0_CLIENT_ID | The client ID from your auth0 application. This can be found on the applications page on your Auth0 account
AUTH0_CLIENT_SECRET | The client secret from your auth0 application. This can be found on the applications page on your Auth0 account
FLASK_SECRET_KEY | This value is used by flask for signing sessions or something. You can generate it by running `base64.b64encode(os.urandom(50)).decode('utf-8')` in a python3 shell with `os` and `base64` imported. [More Info](http://flask.pocoo.org/docs/1.0/config/#SECRET_KEY)
DATABASE_URL | This is the URL to your database (looks like `mongodb://`). If you are using mlab this should be easily accessible through your account.
MAPS_APIKEY | This is your server API key from the [credentials page](https://console.cloud.google.com/apis/credentials) of your Google Cloud Platform console.

To set an environment variable on mac, run `env VARIABLE_NAME=value` 
on windows run `set VARIABLE_NAME=value`

3. Once variables are set, type `flask run` inside the pipenv environment to run te flask built in development server. You will be provided with a URL where you can view your site on your local machine.
