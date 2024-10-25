from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from typing import List

class ReservationSchema(BaseModel):
    id: int
    validation: bool
    start_date: date
    end_date: date
    user_id: int
    room_ids: List[int]  # List of room IDs for the many-to-many relationship
    
    model_config = ConfigDict(from_attributes=True)  # Replaces orm_mode in Pydantic v2

class ReservationCreate(BaseModel):
    validation: bool = Field(default=False)
    start_date: date
    end_date: date
    user_id: int
    room_ids: List[int]  # IDs of rooms being reserved
