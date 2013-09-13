import os

DEBUG = True

SITE_TITLE = "Daniel 'MaTachi' Jonsson"
REPO_NAME = 'MaTachi.github.io'
POST_SOURCE_ROOT = 'https://github.com/MaTachi/{}/tree/master/src/pages/'.format(REPO_NAME)

APP_DIR = os.path.dirname(os.path.abspath(__file__))

def parent_dir(path):
    '''Return the parent of a directory.'''
    return os.path.abspath(os.path.join(path, os.pardir))

PROJECT_ROOT = parent_dir(APP_DIR)

# Build the static files to the project root
FREEZER_DESTINATION = PROJECT_ROOT
FREEZER_BASE_URL = 'http://localhost/'
# Don't overwrite app files
FREEZER_REMOVE_EXTRA_FILES = False
FLATPAGES_EXTENSION = '.md'
