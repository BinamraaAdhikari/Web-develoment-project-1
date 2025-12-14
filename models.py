from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

    applications = relationship("Application", back_populates="owner")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    company = Column(String)
    role = Column(String)
    status = Column(String, default="Applied")
    created_at = Column(DateTime, default=datetime.utcnow)

    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="applications")
