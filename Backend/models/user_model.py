from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from Backend.config.db import Base

class User(Base):
    __tablename__ = "users"
    email = Column(String(255), primary_key=True, index=True)



    blogs = relationship("Blog", back_populates="author", cascade="all, delete")
    comments = relationship("Comment", back_populates="author", cascade="all, delete")
