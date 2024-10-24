from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Classes.Room import Room
from database import SessionLocal
from typing import List
from PydanticModels.pydantic_model_room import RoomCreate , RoomSchema

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router.get("/", response_model=List[RoomSchema])
def get_Rooms(db: Session = Depends(get_db)):
    rooms = db.query(Room).all()
    return rooms