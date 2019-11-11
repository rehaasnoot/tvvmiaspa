#!/usr/bin/env python3

from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType
from tvvmiaecology.models import LoginModel, RoleModel, PlayerModel, InstrumentModel, OrderModel

TVVObjectType = SQLAlchemyObjectType

#class TVVObjectType(SQLAlchemyObjectType):
#    class Meta:
#        abstract = True
#        interfaces = (relay.Node, )

class Login(TVVObjectType):
    class Meta:
        model = LoginModel
        interfaces = (relay.Node, )

class Role(TVVObjectType):
    class Meta:
        model = RoleModel
        interfaces = (relay.Node, )

class Player(TVVObjectType):
    class Meta:
        model = PlayerModel
        interfaces = (relay.Node, )

class Instrument(TVVObjectType):
    class Meta:
        model = InstrumentModel
        interfaces = (relay.Node, )

class Order(TVVObjectType):
    class Meta:
        model = OrderModel
        interfaces = (relay.Node, )

