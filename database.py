from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_declarative import Restaurant, User

Base = declarative_base()

user = 'texas'
password = 'texas'
database_host = 'hacksql.viasat.io'
engine = create_engine(
    'mysql+mysqlconnector://{}:{}@{}/texas'.format(user, password, database_host))
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
metadata = MetaData()