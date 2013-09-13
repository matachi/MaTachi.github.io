from flask import Blueprint, render_template, abort
from flask_flatpages import FlatPages
from ..app import pages

blog = Blueprint('blog', __name__, template_folder='templates')

@blog.route('/')
def index():
    pages_sorted = sorted(pages, reverse=True,
                          key=lambda p: p.meta['published'])
    return render_template('blog/index.html', pages=pages_sorted, active='blog')

@blog.route('/<path:path>/')
def page(path):
    page = pages.get_or_404(path)
    return render_template('blog/page.html', page=page, active='blog')
