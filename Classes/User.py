from sqlalchemy import Column, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = 'users'  # Make sure this matches the ForeignKey

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    is_admin = Column(Boolean)
    hashed_password = Column(String(255))

    # Relationships
    reservations = relationship('Reservation', back_populates='user')
