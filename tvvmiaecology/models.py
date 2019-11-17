import uuid
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from flask_security import UserMixin, RoleMixin
from .database import db_session_scoped

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

class RoleModel(TVVBase, TVVModelAux, RoleMixin):
    __tablename__ = 'tvvrole'
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    uuid = Column('uuid', String, nullable=False, default=newUUID(__tablename__))
    name = Column('name', String, nullable=False, unique=True)
    #login = relationship('LoginModel', backref=backref('role_id'))
    
class LoginModel(TVVBase, TVVModelAux, UserMixin):
    __tablename__ = 'tvvlogin'
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    email = Column('email', String, nullable=False)
    password = Column('password', String, nullable=False)
    uuid = Column('uuid', String, nullable=False, default=newUUID(__tablename__))
    signed_up_on = Column('signed_up_on', DateTime, nullable=False, default=func.now())
    first_name = Column('first_name', String, nullable=False)
    last_name = Column('last_name', String, nullable=False)
    address_street = Column('address_street', String)
    address_city = Column('address_city', String)
    address_state = Column('address_state', String)
    address_zip = Column('address_zip', String)
    phone_number = Column('phone_number', String, nullable=False)
    role_id = Column('role_id', ForeignKey('tvvrole.id'))
    role = relationship( 'RoleModel', backref=backref('role_id', uselist=True))
    #user_id = relationship('UserModel', backref=backref(''))
    #users = relationship('UserModel', )
    def __repr__(self):
        return "{}".format(self.email)

class PlayerModel(TVVBase, TVVModelAux):
    __tablename__ = 'tvvplayer'
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    uuid = Column('uuid', String, nullable=False, default=newUUID(__tablename__))
    name = Column('name', String, nullable=False)
    description = Column('description', String, nullable=False)
    uri = Column('uri', String, nullable=False)
    #players = relationship('OrderModel', backref='player')
#    orders = relationship('OrderModel', back_populates='player')
class InstrumentModel(TVVBase, TVVModelAux):
    __tablename__ = 'tvvinstrument'
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    uuid = Column('uuid', String, nullable=False, default=newUUID(__tablename__))
    name = Column('name', String, nullable=False)
    description = Column('description', String, nullable=False)
    uri = Column('uri', String, nullable=False)

class OrderModel(TVVBase, TVVModelAux):
    __tablename__ = 'tvvorder'
    id = Column('id', Integer, primary_key=True, nullable=False, autoincrement=True)
    uuid = Column('uuid', String, nullable=False, default=newUUID(__tablename__))
    blender_uri = Column('blender_uri', String, nullable=False)
    midi_uri = Column('midi_uri', String, nullable=False)
    login_id = Column('login_id', ForeignKey('tvvlogin.id'))
    login = relationship('LoginModel', backref=backref('login_id', uselist=True))
    player_id = Column('player_id', ForeignKey('tvvplayer.id'))
    player = relationship('PlayerModel', backref=backref('player_id', uselist=True))
    def __repr__(self):
        return "{}".format(self.id)

#Flask-Security
login_role = relationship('LoginModel', secondary=('RoleModel'))

#user_role = Table('tvv_user_role', SQLAlchemyObjectType().Meta, Column('login_id', ForeignKey('tvvlogin.id'), primary_key=True), Column('role_id', ForeignKey('tvvrole.id'), primary_key=True) )
if INITIALIZE_DATABASE:
    from .database import db_engine
    TVVBase.metadata.create_all(bind=db_engine)
    db_session_scoped().commit

