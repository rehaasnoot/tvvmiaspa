from .__init__ import *

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

