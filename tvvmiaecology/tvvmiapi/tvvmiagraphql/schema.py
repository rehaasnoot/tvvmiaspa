from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from ...models import RoleModel, LoginModel, PlayerModel, InstrumentModel, OrderModel

class Role(SQLAlchemyObjectType):
    class Meta:
        model = RoleModel
        interfaces = (relay.Node, )

class Login(SQLAlchemyObjectType):
    class Meta:
        model = LoginModel
        interfaces = (relay.Node, )

class Player(SQLAlchemyObjectType):
    class Meta:
        model = PlayerModel
        interfaces = (relay.Node, )

class Instrument(SQLAlchemyObjectType):
    class Meta:
        model = InstrumentModel
        interfaces = (relay.Node, )

class Order(SQLAlchemyObjectType):
    class Meta:
        model = OrderModel
        interfaces = (relay.Node, )

