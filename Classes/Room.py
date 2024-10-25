from sqlalchemy import Boolean, Column, Integer, Date, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

class Room(Base):
    __tablename__ = 'rooms'  # Plural table name

    # Association table for many-to-many relationship with Reservation
    reservation_room_association = Table(
        'reservation_room_association',
        Base.metadata,
        Column('reservation_id', Integer, ForeignKey('reservations.id'), primary_key=True),
        Column('room_id', Integer, ForeignKey('rooms.id'), primary_key=True)
    )

    id = Column(Integer, primary_key=True, index=True)
    number = Column(Integer, unique=True, index=True)
    vip = Column(Boolean, default=False)
    price = Column(Integer)
    available = Column(Boolean, default=True)
    start_time = Column(Date)
    end_time = Column(Date)
    number_of_beds = Column(Integer)

    # Foreign key to establish many-to-one relationship with Hotel
    hotel_id = Column(Integer, ForeignKey('hotels.id'))  # Use plural name

    # Relationship to the Hotel model (many-to-one)
    hotel = relationship('Hotel', back_populates='rooms')

    # Many-to-many relationship with Reservation
    reservations = relationship('Reservation', secondary=reservation_room_association, back_populates='rooms')

    @property
    def duration(self):
        """Calculate the duration of stay based on start and end times."""
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).days
        return None
