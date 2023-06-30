from sqlalchemy import Column, String, Boolean, Integer, Text
from db_setup import Base


class Users(Base):
    __tablename__= "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(200), unique=True, index=True)
    username = Column(String(500), index=True)
    password = Column(Text)
    is_active = Column(Boolean, default=True, index=True)
    is_superuser = Column(Boolean, default=False)
    
    def __repr__(self):
        return 'User %s' % self.name
    
