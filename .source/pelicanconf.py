#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Jack Minardi'
SITENAME = u'jack.minardi.org'
SITEURL = u'http://jack.minardi.org'

TIMEZONE = 'Europe/Paris'
DEFAULT_LANG = u'en'

THEME = '/Users/jminardi/pelican-themes/mnmlist'

PAGE_URL = '{slug}'
PAGE_SAVE_AS = '{slug}/index.html'
ARTICLE_URL = '{category}/{slug}'
ARTICLE_SAVE_AS = '{category}/{slug}/index.html'
CATEGORY_URL = '{slug}'
CATEGORY_SAVE_AS = '{slug}/index.html'

GOOGLE_ANALYTICS = 'UA-42321662-1'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
FEED_ATOM = None

# Blogroll
#LINKS = (('Pelican', 'http://getpelican.com/'),
#         ('Python.org', 'http://python.org/'),
#         ('Jinja2', 'http://jinja.pocoo.org/'),
#         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('twitter', 'https://www.twitter.com/jackminardi'),
          ('github', 'https://www.github.com/jminardi'),
          ('linkedin', 'http://www.linkedin.com/in/jackminardi'),
    )

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
