from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import *


Base = declarative_base()


class Restaurant(Base):
    __tablename__ = 'restaurants'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    category = Column(String(50), nullable=False)
    votes = Column(Integer, nullable=False)


class User(Base):
    __tablename__ = 'user'
    username = Column(String(50), primary_key=True)
    rest_id = Column(Integer, ForeignKey('restaurants.id'), nullable=True)
    voted = Column(Boolean, nullable=False)


class UserList(Base):
    __tablename__ = 'userlist'
    username = Column(String(50), primary_key=True)


class Blacklist(Base):
    __tablename__ = 'blacklist'
    name = Column(String(50), primary_key=True)

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.

user = 'wayne'
password = 'password'
database_host = '10.0.1.209'
engine = create_engine(
    'mysql+mysqlconnector://{}:{}@{}/hackathon'.format(user, password, database_host))
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
metadata = MetaData()

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
