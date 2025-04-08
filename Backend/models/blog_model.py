from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from Backend.config.db import Base

class Blog(Base):
    __tablename__ = "blogs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(String(5000), nullable=False)
    
    author_email = Column(String(255), ForeignKey("users.email"))


    author = relationship("User", back_populates="blogs")
    comments = relationship("Comment", back_populates="blog", cascade="all, delete")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(2000), nullable=False)
    blog_id = Column(Integer, ForeignKey("blogs.id"), nullable=False)
    author_email = Column(String(255), ForeignKey("users.email"))

    blog = relationship("Blog", back_populates="comments")
    author = relationship("User", back_populates="comments")