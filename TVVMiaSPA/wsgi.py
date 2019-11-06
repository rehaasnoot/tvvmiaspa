#!/usr/bin/env python

from tvvmiaweb import urls
from tvvmiaweb import config

# app = GUnicorn Hook
app = urls.app
app.config['DEBUG'] = config.DEBUG
