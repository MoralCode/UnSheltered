# UnSheltered
 An online listing and occupancy tracking system for homeless shelters. The homelessness crisis in Portland continues to increase with 57% being unsheltered. The goal of our website is to allow the local homeless to find shelters with enough spaces and that has needed amenities. In addition, our app educates homeless youth on their educational rights as well as advertising volunteer opportunities for local community members or homeless that want to give back to shelters.




## Setup
1. [Download and Install Python 3.x](https://www.python.org/downloads/) and check the box in the installer to add it to your PATH
2. `cd ` into the project (if on windows use cmd)
3. `pip install pipenv` or `python -m pip install pipenv`
> If pipenv isn’t available in your shell after installation, you’ll need to add the user base’s binary directory to your PATH.

https://docs.pipenv.org/install/#installing-pipenv

3. `pipenv sync`


# Run development server
[Source](https://github.com/pallets/flask)
run `pipenv shell` to enter a shell in the local environment (with all the dependencies and such)

if on mac run `env FLASK_APP=backend.py flask run` 
if on windows run `set FLASK_APP=backend.py` then `flask run` 

you should be provided with the URL for the local development server

use the environment variable `FLASK_ENV=development` to enable development mode so you dont have to restart flask every time you make a change
