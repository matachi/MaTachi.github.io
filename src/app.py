from flask import Flask, render_template
from flask_flatpages import FlatPages

app = Flask(__name__)
app.config.from_pyfile('config.py')
pages = FlatPages(app)

from blog.views import blog
app.register_blueprint(blog, url_prefix='/blog')

from views import *
