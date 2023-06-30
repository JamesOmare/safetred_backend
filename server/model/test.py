

from typing import List, Optional
from sqlalchemy import Column, String, Boolean, Integer, Text
from sqlmodel import SQLModel, Field, Relationship, DateTime
from ..db_setup import Base
from datetime import datetime

# from datetime import date
# from typing import Optional
# from sqlalchemy import Enum, table
# from sqlmodel import SQLModel, Field, Relationship
# from mixins import TimeMixin


# class Sex(str, Enum):
#     MALE = "MALE"
#     FEMALE = "FEMALE"


# class Person(SQLModel, TimeMixin, table=True):
#     __tablename__ = "person"

#     id: Optional[str] = Field(None, primary_key=True, nullable=False)
#     name: str
#     birth: date
#     sex: Sex
#     profile: str
#     phone_number: str

#     users: Optional["Users"] = Relationship(
#         sa_relationship_kwargs={'uselist': False}, back_populates="person")

# class Users(Base,TimeMixin,table=True):
#     __tablename__= "users"

#     id: int = Field(Integer, primary_key=True, nullable=False)
#     username: str = Field(sa_column=Column("username", String, unique=True))
#     email: str = Field(sa_column=Column("email", String, unique=True))
#     password: str
#     is_active = Column(Boolean, default=True)
#     is_superuser = Column(Boolean, default=False)
#     person_id: Optional[str] = Field(default=None, foreign_key="person.id")
#     person: Optional["Person"] = Relationship(back_populates="users")

#     roles: List["Role"] = Relationship(back_populates="users", link_model=UsersRole)

# class Item(BaseModel):
#     name: str
#     description: str | None = Field(
#         default=None, title="The description of the item", max_length=300
#     )
#     price: float = Field(gt=0, description="The price must be greater than zero")
#     tax: float | None = None

# class Users(Base):
#     __tablename__= "users"
    
#     id = Column(Integer, primary_key=True, index=True)
#     email = Column(String(200), unique=True, index=True)
#     username = Column(String(500), index=True)
#     password = Column(Text)
#     is_active = Column(Boolean, default=True, index=True)
#     is_superuser = Column(Boolean, default=False)
#     created_at : datetime = Field(default_factory=datetime.now)
#     modified_at : datetime = Field(sa_column=Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False))
    
#     def __repr__(self):
#         return 'User %s' % self.name