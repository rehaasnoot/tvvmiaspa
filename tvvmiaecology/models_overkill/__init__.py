import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from flask_security import UserMixin, RoleMixin
from ..database import db_session_scoped

INITIALIZE_DATABASE=False

TVVBase = declarative_base()
declarative_base.query = db_session_scoped

def newUUID(pepper):
    return "{}".format(uuid.uuid5(uuid.NAMESPACE_DNS, pepper + 'tvvmia.com'))

class TVVModelAux():
    def to_json(self):
        return dict(name=self.name, is_admin=self.is_admin)
    def __repr__(self):
        return "{}".format(self.name)

#Flask-Security
login_role = relationship('LoginModel', secondary=('RoleModel'))

#user_role = Table('tvv_user_role', SQLAlchemyObjectType().Meta, Column('login_id', ForeignKey('tvvlogin.id'), primary_key=True), Column('role_id', ForeignKey('tvvrole.id'), primary_key=True) )
if INITIALIZE_DATABASE:
    from ..database import db_engine
    TVVBase.metadata.create_all(bind=db_engine)
    db_session_scoped().commit

