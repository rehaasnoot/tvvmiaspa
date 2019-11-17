from .__init__ import *

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