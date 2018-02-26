from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


Base = declarative_base()

association_table = Table(
    'user_place_association', Base.metadata,
    Column('users', String(40), ForeignKey('users.ip')),
    Column('places', String(40), ForeignKey('places.code'))
)


class User(Base):
    def __init__(**kwargs):
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                print "%s == %s" % (key, value)

    __tablename__ = 'users'

    ip = Column(String(40), primary_key=True)
    places = relationship(
        "Place",
        secondary=association_table,
        back_populates="users"
    )


class Place(Base):
    def __init__(**kwargs):
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                print "%s == %s" % (key, value)

    __tablename__ = 'places'

    code = Column(String(40), nullable=False, primary_key=True)
    place = Column(String(20), nullable=False)
    users = relationship(
        "User",
        secondary=association_table,
        back_populates="places"
    )


class Matrix(Base):
    def __init__(**kwargs):
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                print "%s == %s" % (key, value)

    __tablename__ = 'matrix'

    ip = Column(String(40), ForeignKey('users.ip'), primary_key=True)
    choice = Column(String(10), nullable=False)
    user = relationship("User", backref="matrix")
