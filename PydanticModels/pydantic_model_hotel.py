from pydantic import BaseModel
from typing import List, Optional

# Pydantic model for the response
class HotelSchema(BaseModel):
    id: int
    name: str
    type: str
    vol: str
    price: int
    duration: str
    vip: bool
    image_url: Optional[str] = None  # Optional field

    class Config:
        orm_mode = True  # This enables FastAPI to work with SQLAlchemy objects

# Pydantic model for creating a hotel
class HotelCreate(BaseModel):
    name: str
    type: str
    vol: str
    price: int
    duration: str
    vip: bool
    image_url: Optional[str] = None  # Optional field
