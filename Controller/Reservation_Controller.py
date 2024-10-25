from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from Classes.Reservation import Reservation
from database import SessionLocal
from PydanticModels.pydantic_model_reservation import ReservationCreate, ReservationSchema

router_reservation = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get all reservations
@router_reservation.get("/", response_model=List[ReservationSchema])
def get_reservations(db: Session = Depends(get_db)):
    reservations = db.query(Reservation).all()
    return reservations

# Get reservation by ID
@router_reservation.get("/{reservation_id}", response_model=ReservationSchema)
def get_reservation(reservation_id: int, db: Session = Depends(get_db)):
    reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    return reservation

# Create a new reservation
@router_reservation.post("/", response_model=ReservationSchema)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    new_reservation = Reservation(**reservation.dict())
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    return new_reservation

# Update an existing reservation
@router_reservation.put("/{reservation_id}", response_model=ReservationSchema)
def update_reservation(reservation_id: int, reservation: ReservationCreate, db: Session = Depends(get_db)):
    db_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    for key, value in reservation.dict().items():
        setattr(db_reservation, key, value)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

# Delete a reservation
@router_reservation.delete("/{reservation_id}", response_model=dict)
def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    db_reservation = db.query(Reservation).filter(Reservation.id == reservation_id).first()
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    db.delete(db_reservation)
    db.commit()
    return {"message": "Reservation deleted successfully"}
