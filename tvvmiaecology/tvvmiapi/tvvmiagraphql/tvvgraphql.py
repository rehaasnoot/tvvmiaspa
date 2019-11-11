from graphene import Schema
from .queries import TVVQueries
from .mutations import TVVMutations

TVVMiaAPIGraphQL = Schema(query=TVVQueries, mutation=TVVMutations)
