from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

class Hotel(Base):
    __tablename__ = 'hotel'

    user_hotel_association = Table(
        'user_hotel_association',
        Base.metadata,
        Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
        Column('hotel_id', Integer, ForeignKey('hotel.id'), primary_key=True)
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    type = Column(String(100))
    vol = Column(String(50))
    price = Column(Integer)
    duration = Column(String(50))
    vip = Column(Boolean)
    image_url = Column(String(255))

    # Many-to-many relationship with User
    users = relationship('User', secondary=user_hotel_association, back_populates='hotels')

    # One-to-many relationship with Room
    rooms = relationship('Room', back_populates='hotel')
