#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Jack Minardi'
SITENAME = u'jack.minardi.org'
SITEURL = u'http://jack.minardi.org'

DEFAULT_LANG = u'en'
DEFAULT_DATE_FORMAT = '%B %Y'

THEME = 'theme'

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
FEED_ALL_RSS = 'feeds/all.rss.xml'

RELATIVE_URLS = True

STATIC_PATHS = ['images', 'files']

PLUGIN_PATH = './plugins'
PLUGINS = ['ipythonnb']
MARKUP = ('md', 'ipynb')
