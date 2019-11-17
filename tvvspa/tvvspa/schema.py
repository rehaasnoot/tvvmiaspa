import graphene
from graphene_django import DjangoObjectType
from .models import Player, Instrument, Music, Order

class PlayerType(DjangoObjectType):
    class Meta:
        model = Player

class InstrumentType(DjangoObjectType):
    class Meta:
        model = Instrument

class MusicType(DjangoObjectType):
    class Meta:
        model = Music

class OrderType(DjangoObjectType):
    class Meta:
        model = Order


class Query(graphene.ObjectType):
#    players = graphene.List(PlayerType)
#    instruments = graphene.List(InstrumentType)
    orders = graphene.List(OrderType)
    def resolve_orders(self, info):
        return Order.objects.all()

schema = graphene.Schema(query=Query)