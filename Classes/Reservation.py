from sqlalchemy import Boolean, Column, Integer, Date, String, ForeignKey
from sqlalchemy.orm import relationship
from Classes.Room import Room
from Classes.User import User
from database import Base

class Reservation(Base):
    __tablename__ = 'reservations'  # Make sure the table name is plural for consistency

    id = Column(Integer, primary_key=True, index=True)
    validation = Column(Boolean, default=False)  # Indicates if the reservation is validated
    start_date = Column(Date, nullable=False)  # Start date of reservation
    end_date = Column(Date, nullable=False)    # End date of reservation

    # Foreign key to the user who made the reservation
    user_id = Column(Integer, ForeignKey('users.id'))  # Ensure this matches the User table name
    user = relationship('User', back_populates='reservations')

    # Many-to-many relationship with Room through an association table
    rooms = relationship('Room', secondary=Room.reservation_room_association, back_populates='reservations')

    @property
    def total_price(self):
        """Calculate the total price of all rooms in the reservation."""
        return sum(room.price for room in self.rooms if room.price is not None)

    def show_rooms_with_duration(self):
        """Display all rooms in the reservation with their duration."""
        room_details = []
        for room in self.rooms:
            duration = (self.end_date - self.start_date).days  # Calculate duration based on start and end dates
            room_details.append({
                'room_number': room.number,
                'duration': duration,
                'price': room.price,
                'vip': room.vip,
                'available': room.available
            })
        return room_details
