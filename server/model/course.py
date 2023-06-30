# import enum

# from sqlalchemy import Enum, Column, ForeignKey, Integer, String, Text, Boolean
# from sqlalchemy.orm import relationship
# # from sqlalchemy_utils import URLType

# # from ..db_setup import Base
# # from .user import User
# from .mixins import Timestamp
# from sqlalchemy.ext.declarative import declarative_base
# from db_setup import Base
# # Base = declarative_base()
# class ContentType(enum.Enum):
#     lesson = 1
#     quiz = 2
#     assignment = 3


# class Course(Timestamp, Base):
#     __tablename__ = "courses"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(200), nullable=False)
#     description = Column(Text, nullable=True)
#     user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
#     sections = relationship("Section", back_populates="course", uselist=False)
#     student_courses = relationship("StudentCourse", back_populates="course")


# class Section(Timestamp, Base):
#     __tablename__ = "sections"

#     id = Column(Integer, primary_key=True, index=True)
#     title = Column(String(200), nullable=False)
#     description = Column(Text, nullable=True)
#     course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)

#     course = relationship("Course", back_populates="sections")
#     content_blocks = relationship("ContentBlock", back_populates="section")