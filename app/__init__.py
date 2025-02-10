from flask import Flask
from flask_caching import Cache
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
app.config['CACHE_TYPE'] = 'simple'

cache = Cache(app)

from app import routes
