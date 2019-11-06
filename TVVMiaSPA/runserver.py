#!/usr/bin/env python

from tvvmiaweb import views
from tvvmiaweb import models
from tvvmiaweb import config

app = views.app

# Return an App
if __name__ == "__main__":
    views.app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
