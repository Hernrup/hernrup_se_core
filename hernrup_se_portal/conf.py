#!/usr/bin/env python
from __future__ import unicode_literals
import os
import sys

sys.path.append(os.curdir)

AUTHOR = 'Mikael Hernrup'
SITENAME = 'Portal'
SITEURL = 'http://hernrup.github.io/hernrup_se/'

PATH = 'content'
OUTPUT_PATH = '/output/'
DELETE_OUTPUT_DIRECTORY = False
PAGE_PATHS = ['pages']

TIMEZONE = 'Europe/Stockholm'

DEFAULT_LANG = 'en'

LOAD_CONTENT_CACHE = False

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = 'feeds/all.atom.xml'
CATEGORY_FEED_ATOM = 'feeds/%s.atom.xml'
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = []

# Social widget
SOCIAL = (
    ('Github', 'https://github.com/Hernrup'),
    ('LinkedIn', 'https://se.linkedin.com/pub/mikael-hernrup/31/247/624'),
)

DEFAULT_PAGINATION = False
RELATIVE_URLS = True

STATIC_PATHS = [
    'images',
    'extra/robots.txt',
    'extra/favicon.ico'
]
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'}
}

THEME = 'theme/svbhack'
GOOGLE_ANALYTICS = None
DISQUS_SITENAME = 'hernrup_se_portal'
USER_LOGO_URL = './images/site/logo_portal.png'
TAGLINE = 'Under construction'
INTERNET_DEFENSE_LEAGUE = False
