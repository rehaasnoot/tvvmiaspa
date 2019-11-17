from graphene import Schema
from .queries import Queries
from .mutations import Mutations

TVVMiaAPIGraphQL = Schema(query=Queries, mutation=Mutations)
