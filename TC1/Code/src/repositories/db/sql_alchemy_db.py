# Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import configparser
import os
from dotenv import load_dotenv

# Environment variables
load_dotenv()
SQL_ALCHEMY_DATABASE_URL = os.getenv('SQL_ALCHEMY_DATABASE_URL')

engine = create_engine(SQL_ALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()