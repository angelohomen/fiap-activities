# Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import configparser
import os

# Config variables
config = configparser.ConfigParser()
config.read('.env')
SQL_ALCHEMY_DATABASE_URL = config['SQL']['SQL_ALCHEMY_DATABASE_URL']

engine = create_engine(SQL_ALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()