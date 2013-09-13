from flask import render_template

from app import app

@app.route('/')
def index():
    return render_template('index.html', active='index')

@app.route('/contact/')
def contact():
    return render_template('contact.html', active='contact')

@app.context_processor
def utility_processor():
    def page_title(title=None):
        return "{} | {}".format(title, app.config['SITE_TITLE']) if title \
               else app.config['SITE_TITLE']
    def post_source(path):
        return '{}{}{}'.format(app.config['POST_SOURCE_ROOT'],
                               path,
                               app.config['FLATPAGES_EXTENSION'])
    return dict(page_title=page_title, post_source=post_source)

@app.template_filter('date')
def date_filter(date):
    return date.strftime('%B %-d, %Y')
