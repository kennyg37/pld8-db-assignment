from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    
    user_data = relationship("User_data", back_populates="user")

class Countries(Base):
    __tablename__ = 'countries'
    
    id = Column(Integer, primary_key=True)
    country_name = Column(String)

    user_data = relationship("User_data", back_populates="country_rel")

class User_data(Base):
    __tablename__ = 'user_data'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    country_id = Column(Integer, ForeignKey('countries.id'))
    gender = Column(Integer)
    age = Column(Integer)
    annual_salary = Column(Integer)
    credit_card = Column(Integer)
    net_worth = Column(Integer)
    car_purchase = Column(Integer)

    user = relationship("User", back_populates="user_data")
    country_rel = relationship("Countries", back_populates="user_data")
