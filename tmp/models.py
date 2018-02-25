from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    ip = Column(String(40), primary_key=True)
    choice = Column(String(10), nullable=False)
    timestamp = Column(
        DateTime(timezone=True), nullable=False,
        server_default=func.now())

    def __repr__(self):
        return (f"<User ip={self.ip} choice={self.choice}"
                f" timestamp={self.timestamp}>")
