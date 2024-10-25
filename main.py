from fastapi import FastAPI
from database import engine, SessionLocal,Base
from Controller.Room_Controller import router_room
from Controller.Hotel_Controller import router_hotel
from Controller.Reservation_Controller import router_reservation
from Controller.User_Controller import router # Import your User router

app = FastAPI()

# Include routers
app.include_router(router_hotel, prefix="/hotels")
app.include_router(router_room, prefix="/rooms")
app.include_router(router_reservation, prefix="/reservations")
app.include_router(router, prefix="/users")  # Add User router

# Initialize DB tables if not created
Base.metadata.create_all(bind=engine)
