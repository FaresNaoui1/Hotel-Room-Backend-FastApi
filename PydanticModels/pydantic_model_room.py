from pydantic import BaseModel

class RoomSchema(BaseModel):
    id: int
    number: int
    vip: bool
    price: float
    available: bool
    start_time: str  # or date type if you want to parse as date
    end_time: str
    number_of_beds: int
    hotel_id: int

    class Config:
        from_attributes = True  # Replaces `orm_mode` in Pydantic V2

class RoomCreate(BaseModel):
    number: int
    vip: bool
    price: float
    available: bool
    start_time: str
    end_time: str
    number_of_beds: int
    hotel_id: int
