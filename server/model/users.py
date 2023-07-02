from sqlalchemy import Column, String, Boolean, Integer, Text
from db_setup import Base
from .mixins import Timestamp

class Users(Timestamp, Base):
    __tablename__= "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(200), unique=True, index=True)
    username = Column(String(500), index=True)
    password = Column(Text)
    phone_number: str = Column(String(20), index=True)
    is_active = Column(Boolean, default=True, index=True)
    is_superuser = Column(Boolean, default=False)
    
    def __repr__(self):
        return 'User %s' % self.name
    
    class Config:
        schema_extra = {
            "example": {
                "email": "test@gmail.com.",
                "username": "test_master",
                "password": "test1234",
                "phone_number": "254792310042",
                "is_active": True,
                "is_superuser": False
                
            }
        }
    
