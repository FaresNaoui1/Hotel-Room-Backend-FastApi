from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Classes.Hotel import Hotel
from database import SessionLocal
from typing import List
from PydanticModels.pydantic_model_hotel import HotelSchema, HotelCreate  # Import the Pydantic models

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all hotels
@router.get("/", response_model=List[HotelSchema])
async def get_hotels(db: Session = Depends(get_db)):
    hotels = db.query(Hotel).all()
    return hotels  # SQLAlchemy models will be converted to Pydantic models automatically

# Create a new hotel
@router.post("/", response_model=HotelSchema)
async def add_hotel(hotel: HotelCreate, db: Session = Depends(get_db)):
    new_hotel = Hotel(
        name=hotel.name,
        type=hotel.type,
        vol=hotel.vol,
        price=hotel.price,
        duration=hotel.duration,
        vip=hotel.vip,
        image_url=hotel.image_url
    )
    db.add(new_hotel)
    db.commit()
    db.refresh(new_hotel)
    return new_hotel  # Return the created hotel
