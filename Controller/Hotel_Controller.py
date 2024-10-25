from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from Classes.Hotel import Hotel
from database import SessionLocal
from PydanticModels.pydantic_model_hotel import HotelCreate, HotelSchema

router_hotel = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all hotels
@router_hotel.get("/", response_model=List[HotelSchema])
def get_hotels(db: Session = Depends(get_db)):
    hotels = db.query(Hotel).all()
    return hotels

# Get hotel by ID
@router_hotel.get("/{hotel_id}", response_model=HotelSchema)
def get_hotel(hotel_id: int, db: Session = Depends(get_db)):
    hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    return hotel

# Create a new hotel
@router_hotel.post("/", response_model=HotelSchema)
def create_hotel(hotel: HotelCreate, db: Session = Depends(get_db)):
    new_hotel = Hotel(**hotel.dict())
    db.add(new_hotel)
    db.commit()
    db.refresh(new_hotel)
    return new_hotel

# Update an existing hotel
@router_hotel.put("/{hotel_id}", response_model=HotelSchema)
def update_hotel(hotel_id: int, hotel: HotelCreate, db: Session = Depends(get_db)):
    db_hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if db_hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    for key, value in hotel.dict().items():
        setattr(db_hotel, key, value)
    db.commit()
    db.refresh(db_hotel)
    return db_hotel

# Delete a hotel
@router_hotel.delete("/{hotel_id}", response_model=dict)
def delete_hotel(hotel_id: int, db: Session = Depends(get_db)):
    db_hotel = db.query(Hotel).filter(Hotel.id == hotel_id).first()
    if db_hotel is None:
        raise HTTPException(status_code=404, detail="Hotel not found")
    db.delete(db_hotel)
    db.commit()
    return {"message": "Hotel deleted successfully"}
