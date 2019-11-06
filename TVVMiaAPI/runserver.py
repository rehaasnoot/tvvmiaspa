from flask_api import FlaskAPI
from flask import jsonify
from flask_graphql import GraphQLView

app = FlaskAPI(__name__)

API_FORMAL_NAME = 'TVVMia'
API_NAME = 'tvvmia'
API_ROUTE_ROOT = '/' + API_NAME
API_ROUTE_ARMATURE_LIST = API_ROUTE_ROOT + '/armlist'
API_ROUTE__LIST = API_ROUTE_ROOT + '/'
API_ROUTE_ASSEMBLY_ROOT = API_ROUTE_ROOT + '/assemble'
API_ROUTE_ASSEMBLY_INITIATE = API_ROUTE_ASSEMBLY_ROOT + '/init/<blenderfile><midifile><instrumentname>'
API_ROUTE_ASSEMBLY_CANCEL = API_ROUTE_ASSEMBLY_ROOT + '/cancel/<id>'
API_ROUTE_ASSEMBLY_STATUS = API_ROUTE_ASSEMBLY_ROOT + '/status/<id>'

### GraphQL Support
#app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
# Optional, for adding batch query support (used in Apollo-Client)
#app.add_url_rule('/graphql/batch', view_func=GraphQLView.as_view('graphql', schema=schema, batch=True))

@app.route('/example/')
def example():
    return {'Hello': 'example!'}

@app.route(API_ROUTE_ROOT)
def apiRoot():
    return {'Greetings': 'From ' + API_FORMAL_NAME}

@app.route(API_ROUTE_ARMATURE_LIST)
def apiArmatureList():
    TEST_ARM_1 = {'armature':'armature.name.001', 'object':'object.name.001'}
    TEST_ARM_2 = {'armature':'armature.name.002', 'object':'object.name.002'}
    TEST_ARM_3 = {'armature':'armature.name.003', 'object':'object.name.003'}
    TEST_ARM_LIST = [ TEST_ARM_1, TEST_ARM_2, TEST_ARM_3 ]
    return jsonify(TEST_ARM_LIST)

@app.route(API_ROUTE_ASSEMBLY_INITIATE)
def apiInitiate():
    TEST_ARM_1 = {'armature':'armature.name.001', 'object':'object.name.001'}
    TEST_ARM_2 = {'armature':'armature.name.002', 'object':'object.name.002'}
    TEST_ARM_3 = {'armature':'armature.name.003', 'object':'object.name.003'}
    TEST_ARM_LIST = [ TEST_ARM_1, TEST_ARM_2, TEST_ARM_3 ]
    return jsonify(TEST_ARM_LIST)

if __name__ == "__main__":
    app.run(debug=True)
