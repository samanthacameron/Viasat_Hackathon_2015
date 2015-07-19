import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

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
engine = create_engine('sqlite:///texas.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
