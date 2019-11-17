from graphene import relay , Boolean , String , Field , Mutation , ObjectType
from .schema import Role
from tvvmiaecology.models import newUUID

class RoleCreate(Mutation):
    class Arguments:
        name = String()

    ok = Boolean()
    role = Field(lambda: Role)

    def mutate(self, root, info, name):
        uuid = newUUID()
        role = Role(name=name)
        ok = True
        return RoleCreate(name=name, ok=ok)

class Mutations(ObjectType):
    """Query objects for GraphQL API."""
    #node = relay.Node.Field()
    newRole = relay.Node.Field(RoleCreate)
