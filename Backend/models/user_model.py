from sqlalchemy import Column, String
from Backend.config.db import Base

class User(Base):
    __tablename__ = "users"
    email = Column(String(255), primary_key=True, index=True)
