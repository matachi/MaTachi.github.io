from flask import Flask
from flask_flatpages import FlatPages
from flask_frozen import Freezer

app = Flask(__name__)
app.config.from_pyfile('config.py')
pages = FlatPages(app)
freezer = Freezer(app)

from blog.views import blog
app.register_blueprint(blog, url_prefix='/blog')

from views import *
