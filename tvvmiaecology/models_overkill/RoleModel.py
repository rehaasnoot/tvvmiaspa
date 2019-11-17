from . import TVVBase, TVVModelAux, RoleMixin, newUUID, Column, Integer, String

class RoleModel(TVVBase, TVVModelAux, RoleMixin):
    __tablename__ = 'tvvrole'
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    uuid = Column('uuid', String, nullable=False, default=newUUID(__tablename__))
    name = Column('name', String, nullable=False, unique=True)
    #login = relationship('LoginModel', backref=backref('role_id'))
