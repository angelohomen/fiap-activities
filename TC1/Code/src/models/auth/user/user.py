from src.repositories.db.sql_alchemy_db import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique = True)
    hashed_password = Column(String)