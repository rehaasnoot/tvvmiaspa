
from graphene import relay, ObjectType
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from .schema import Role, Login, Player, Instrument, Order

TVVObjectType = SQLAlchemyObjectType

class TVVQueries(ObjectType):

    """Query objects for GraphQL API."""

    #node = relay.Node.Field()
    login = relay.Node.Field(Login)
    logins = SQLAlchemyConnectionField(Login)
    role = relay.Node.Field(Role)
    roles = SQLAlchemyConnectionField(Role)
    player = relay.Node.Field(Player)
    players = SQLAlchemyConnectionField(Player)
    instrument = relay.Node.Field(Instrument)
    instruments = SQLAlchemyConnectionField(Instrument)
    order = relay.Node.Field(Order)
    orders = SQLAlchemyConnectionField(Order)

