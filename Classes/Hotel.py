from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Hotel(Base):
    __tablename__ = 'hotels'  # Plural table name

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    type = Column(String(100))
    location = Column(String(50))
    rating = Column(Integer)
    description = Column(String(255))  # Increased length for description
    image_url = Column(String(255))

    # One-to-many relationship with Room
    rooms = relationship('Room', back_populates='hotel')
