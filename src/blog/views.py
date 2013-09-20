from urlparse import urljoin
from flask import Blueprint, render_template, request
from flask_flatpages import FlatPages
from werkzeug.contrib.atom import AtomFeed
from ..app import pages, app

blog = Blueprint('blog', __name__, template_folder='templates')

@blog.route('/')
def index():
    pages_sorted = sorted(pages, reverse=True,
                          key=lambda p: p.meta['published'])
    return render_template('blog/index.html', pages=pages_sorted, active='blog')

@blog.route('/<path:path>/')
def page(path):
    path = path.split('/')[-1]
    page = pages.get_or_404(path)
    return render_template('blog/page.html', page=page, active='blog')

@blog.route('/feed.atom')
def feed():
    feed = AtomFeed(
            app.config['SITE_TITLE'], url=app.config['SITE_URL'],
            feed_url='{}/blog/feed.atom'.format(app.config['SITE_URL']))
    recent_pages = sorted(pages, reverse=True,
                          key=lambda p: p.meta['published'])[:15]
    for page in recent_pages:
        feed.add(
            title=page['title'],
            content=unicode(page.html),
            content_type='html',
            author=app.config['AUTHOR'],
            url='{}/blog/{}'.format(app.config['SITE_URL'],
                                    post_path(page['published'], page.path)),
            updated=page['published'],
            published=page['published'])
    return feed.get_response()

def post_path(date, path):
    return '{}/{}'.format(date.strftime('%Y/%m/%d'), path)

@blog.context_processor
def utility_processor():
    return dict(post_path=post_path)
