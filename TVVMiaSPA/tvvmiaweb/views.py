#!/usr/bin/env python

from flask import Flask
from flask import request
from flask import render_template

from tvvmiaweb import config
from tvvmiaweb.models import *
from tvvmiaweb.controllers import hello

app = Flask(__name__)

ROUTE_TEMPLATE_INDEX = [ "/", "starter-template.html" ]
ROUTE_TEMPLATE_FLUID = [ "/fluid", "fluid.html" ]
ROUTE_TEMPLATE_HERO = [ "/hero", "hero.html" ]
ROUTE_TEMPLATE_LAYOUT = [ "/layout", "layout-template.html" ]

# All views below
@app.route(ROUTE_TEMPLATE_INDEX[0])
def index():

    return render_template(ROUTE_TEMPLATE_INDEX[1])

@app.route(ROUTE_TEMPLATE_FLUID[0])
def fluid():

    return render_template(ROUTE_TEMPLATE_FLUID[1])

@app.route(ROUTE_TEMPLATE_HERO[0])
def hero():

    return render_template(ROUTE_TEMPLATE_HERO[1])

@app.route(ROUTE_TEMPLATE_LAYOUT[0])
def layout():

    return render_template(ROUTE_TEMPLATE_LAYOUT[1])


# Error Pages
@app.errorhandler(500)
def error_page(e):
    return render_template('error_pages/500.html'), 500

@app.errorhandler(404)
def not_found(e):
    return render_template('error_pages/404.html'), 404

# Lazy Views
app.add_url_rule('/hello', view_func=hello.hello_world)



