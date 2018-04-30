import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask_login import UserMixin

 
Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(250), nullable=False)
    password = Column(String(94), nullable=False)
    usertype = Column(String(2), nullable=False)


class UserInfo(Base):
    __tablename__ = 'info'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    dob = Column(String(10))
    batch = Column(String(3))
    course = Column(String(3))
    blood_group = Column(String(6))
    mobile = Column(String(13))
    fathers_name = Column(String(80))
    emergency_contact = Column((String(13)))
    userId = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

class Attendance(Base):
    __tablename__ = 'attend'

    id = Column(Integer, primary_key = True)
    Math_p = Column(Integer)
    Math_t = Column(Integer)
    Science_p = Column(Integer)
    Science_t = Column(Integer)
    Art_p = Column(Integer)
    Art_t = Column(Integer)
    English_p = Column(Integer)
    English_t = Column(Integer)
    userId = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

class Slides(Base):
	__tablename__ = "slides"

	id = Column(Integer, primary_key = True)
	slideName = Column(String(30))
	batch = Column(String(3))



engine = create_engine('sqlite:///user-records.db')


Base.metadata.create_all(engine)

#We added this serialize function to be able to send JSON objects in a serializable format
@property
def serialize(self):
   return {
       'name'         : self.name,
       'password'         : self.password,
       'id'         : self.id,
   }
 

engine = create_engine('sqlite:///user-records.db')
 
Base.metadata.create_all(engine)
