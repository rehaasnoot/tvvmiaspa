#!/usr/bin/env python3
from flask import Flask
from flask_graphql import GraphQLView
#from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from tvvmiaecology.config import TVVConfigApi
from flask_security import Security, SQLAlchemySessionUserDatastore

from tvvmiaecology.database import db_session_scoped
from tvvmiaecology.models import LoginModel, RoleModel, PlayerModel, InstrumentModel, OrderModel
from tvvmiaecology.tvvmiapi.tvvmiagraphql.tvvgraphql import TVVMiaAPIGraphQL

ENABLE_SECURITY=False
ENABLE_ADMIN=True
ENABLE_GRAPHQL=True

CONFIG_SECTION = 'TVVMia API GraphQL'
app = Flask(__name__)
CONFIG = TVVConfigApi()
app.debug = CONFIG.get(CONFIG_SECTION, "debug")
app.config['SQLALCHEMY_DATABASE_URI'] = CONFIG.get(CONFIG_SECTION, 'db_uri')
app.config['SECRET_KEY'] = CONFIG.get(CONFIG_SECTION, 'secret_db_key')
API_NAME = CONFIG.get(CONFIG_SECTION, "apiname")
API_ROUTE = '/' + API_NAME
GRAPHQL_ROUTE = API_ROUTE + '/graphql'
ADMIN_ROUTE = API_ROUTE + '/admin'

GREETING="Hello There!  Welcome to the TVVMia GraphQL API!"
### Application Routing ###
def routeUsage():
    return GREETING

@app.route( '/' )
def routeRoot():
    return routeUsage()

@app.route( API_ROUTE )
def routeGreeting():
    return routeUsage()

### Flask-Security
if ENABLE_SECURITY:
    tvvDatastore = SQLAlchemySessionUserDatastore(db_session_scoped, LoginModel, RoleModel)
    tvvSecurity = Security(app, tvvDatastore)

### GraphQL
if ENABLE_GRAPHQL:
    print("Starting GraphQL @ [{}]...".format(GRAPHQL_ROUTE))
    GREETING = GREETING + "<br><a href='{}'>GraphiQL here:</a><br>".format(GRAPHQL_ROUTE)
    viewFunc = GraphQLView(schema=TVVMiaAPIGraphQL).as_view(API_NAME, schema=TVVMiaAPIGraphQL, graphiql=True, get_context=lambda: {'session':db_session_scoped} )
    app.add_url_rule(GRAPHQL_ROUTE, view_func = viewFunc)
    #app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True, get_context=lambda: {'session':Session()}))

### Flask-Admin
if ENABLE_ADMIN:
    print("Starting Flask-Admin @ [{}]...".format(ADMIN_ROUTE))
    GREETING = GREETING + "<br><a href='{}'>Admin here:</a><br>".format(ADMIN_ROUTE)
    tvvAdmin = Admin(app=app, name=ADMIN_ROUTE, 
            url=ADMIN_ROUTE, subdomain=None, 
            index_view=None, 
            translations_path=None, 
            endpoint=None, 
            static_url_path=None, 
            base_template=None, 
            template_mode=None, 
            category_icon_classes=None)
    
    tvvAdmin.add_view(ModelView(LoginModel, db_session_scoped))
    tvvAdmin.add_view(ModelView(RoleModel, db_session_scoped))
    tvvAdmin.add_view(ModelView(PlayerModel, db_session_scoped))
    tvvAdmin.add_view(ModelView(InstrumentModel, db_session_scoped))
    tvvAdmin.add_view(ModelView(OrderModel, db_session_scoped))

@app.teardown_appcontext
def shutdown_session(exception=None):
    #from .models import db_session_scoped
    db_session_scoped.remove()

if __name__ == '__main__':
    thisHost = CONFIG.get(CONFIG_SECTION, "host")
    thisPort = CONFIG.get(CONFIG_SECTION, "port")
    app.run(thisHost, thisPort)

