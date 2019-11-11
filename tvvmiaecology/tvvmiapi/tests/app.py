from flask import Flask
from flask_graphql import GraphQLView
from schema import Schema
from graphql import GraphQLCachedBackend
# from quiver.backend import GraphQLQuiverBackend

def create_app(path='/graphql', **kwargs):
    # backend = GraphQLCachedBackend(GraphQLQuiverBackend({"async_framework": "PROMISE"}))
    backend = None
    api = Flask(__name__)
    api.debug = True
    api.add_url_rule(path, view_func=GraphQLView.as_view('graphql', schema=Schema, backend=backend, **kwargs))
    return api


if __name__ == '__main__':
    api = create_app(graphiql=True)
    api.run()
