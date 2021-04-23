from flask import Flask
import os
#from config import Config
app = Flask(__name__)
#app.config.from_object(Config)


from app import route
from app import db
from app import query

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


"""
1. run route.py --> need to "from app import route" (app is a package)
No need "config.py" ?? 

2. export FLASK_APP=main.py (or any python file storing "app = FLASK(__name__)

3. Need to provide a "secret key" (flask's rule :v)
"""