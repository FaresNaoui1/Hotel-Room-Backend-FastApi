from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from Classes.Room import Room
from database import SessionLocal
from PydanticModels.pydantic_model_room import RoomCreate, RoomSchema
from datetime import date

router_room = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all rooms
@router_room.get("/", response_model=List[RoomSchema])
def get_rooms(db: Session = Depends(get_db)):
    rooms = db.query(Room).all()
    return rooms

# Get room by ID
@router_room.get("/{room_id}", response_model=RoomSchema)
def get_room(room_id: int, db: Session = Depends(get_db)):
    room = db.query(Room).filter(Room.id == room_id).first()
    if room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    return room

# Create a new room
@router_room.post("/", response_model=RoomSchema)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    new_room = Room(**room.dict())
    db.add(new_room)
    db.commit()
    db.refresh(new_room)
    return new_room

# Update an existing room
@router_room.put("/{room_id}", response_model=RoomSchema)
def update_room(room_id: int, room: RoomCreate, db: Session = Depends(get_db)):
    db_room = db.query(Room).filter(Room.id == room_id).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    for key, value in room.dict().items():
        setattr(db_room, key, value)
    db.commit()
    db.refresh(db_room)
    return db_room

# Delete a room
@router_room.delete("/{room_id}", response_model=dict)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    db_room = db.query(Room).filter(Room.id == room_id).first()
    if db_room is None:
        raise HTTPException(status_code=404, detail="Room not found")
    db.delete(db_room)
    db.commit()
    return {"message": "Room deleted successfully"}

# Get rooms by VIP status
@router_room.get("/vip/{vip_status}", response_model=List[RoomSchema])
def get_rooms_by_vip(vip_status: bool, db: Session = Depends(get_db)):
    rooms = db.query(Room).filter(Room.vip == vip_status).all()
    return rooms

# Get rooms by availability
@router_room.get("/available/{availability}", response_model=List[RoomSchema])
def get_rooms_by_availability(availability: bool, db: Session = Depends(get_db)):
    rooms = db.query(Room).filter(Room.available == availability).all()
    return rooms

# Get rooms by number of beds
@router_room.get("/beds/{num_beds}", response_model=List[RoomSchema])
def get_rooms_by_beds(num_beds: int, db: Session = Depends(get_db)):
    rooms = db.query(Room).filter(Room.number_of_beds == num_beds).all()
    return rooms

# Get rooms by price range
@router_room.get("/price/", response_model=List[RoomSchema])
def get_rooms_by_price(min_price: float, max_price: float, db: Session = Depends(get_db)):
    rooms = db.query(Room).filter(Room.price.between(min_price, max_price)).all()
    return rooms

# Get rooms by duration of stay
@router_room.get("/duration/", response_model=List[RoomSchema])
def get_rooms_by_duration(min_days: int, max_days: int, db: Session = Depends(get_db)):
    rooms = db.query(Room).all()
    filtered_rooms = [
        room for room in rooms if room.duration and min_days <= room.duration <= max_days
    ]
    return filtered_rooms
