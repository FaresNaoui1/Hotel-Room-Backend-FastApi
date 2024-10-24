from sqlalchemy import Column, ForeignKey, Integer, String,Table
from sqlalchemy.orm import relationship

from database import Base


# Ensure this import is correct

class User(Base):
    __tablename__ = 'users'

 
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))

    # Relationships
    reservations = relationship('Reservation', back_populates='user')
    hotels = relationship('Hotel', secondary='hotel_user_association', back_populates='users')  # Ensure the secondary table is correct
