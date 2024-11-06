from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
from sqlalchemy.dialects.postgresql import UUID

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String)
    
    user_data = relationship("User_data", back_populates="user")

class Countries(Base):
    __tablename__ = 'countries'
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    country_name = Column(String)

    user_data = relationship("User_data", back_populates="country_rel")

class User_data(Base):
    __tablename__ = 'user_data'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    country_id = Column(UUID(as_uuid=True), ForeignKey('countries.id'))
    gender = Column(String)
    age = Column(Integer)
    annual_salary = Column(Float)
    credit_card = Column(Float)
    net_worth = Column(Float)
    car_purchase = Column(Float)

    user = relationship("User", back_populates="user_data")
    country_rel = relationship("Countries", back_populates="user_data")
