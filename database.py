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
    rest_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)
    voted = Column(Integer, nullable=False)


# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.

user = 'texas'
password = 'texas'
database_host = 'hacksql.viasat.io'
engine = create_engine(
    'mysql+mysqlconnector://{}:{}@{}/texas'.format(user, password, database_host))
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
metadata = MetaData()

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
