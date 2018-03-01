from sqlalchemy import Boolean, Column, ForeignKey, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship


Base = declarative_base()

association_table = Table(
    'user_place_association', Base.metadata,
    Column('users', String(40), ForeignKey('users.ip')),
    Column('places', String(40), ForeignKey('places.code'))
)


class User(Base):
    __tablename__ = 'users'

    ip = Column(String(40), primary_key=True)
    places = relationship(
        "Place",
        secondary=association_table,
        back_populates="users"
    )


class Place(Base):
    __tablename__ = 'places'

    code = Column(String(40), nullable=False, primary_key=True)
    name = Column(String(20), nullable=False)
    filename = Column(String(200), nullable=False)
    users = relationship(
        "User",
        secondary=association_table,
        back_populates="places"
    )


class Sky(Base):

    __tablename__ = 'sky'

    user_ip = Column(String(40), ForeignKey('users.ip'), primary_key=True)
    checked = Column(Boolean, nullable=False)
    user = relationship("User", backref=backref("sky", uselist=False))


class Matrix(Base):
    __tablename__ = 'matrix'

    ip = Column(String(40), ForeignKey('users.ip'), primary_key=True)
    choice = Column(String(10), nullable=False)
    user = relationship("User", backref=backref("matrix", uselist=False))
