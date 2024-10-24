from datetime import datetime

from pydantic import BaseModel
from typing import List, Optional


class RoomSchema(BaseModel):
    id =int
    number =str
    vip = bool
    price = int
    available = bool
    start_time = datetime
    end_time = datetime
    number_of_beds = int


    class Config:
        orm_mode = True


class RoomCreate(BaseModel):
    id = int
    number = str
    vip = bool
    price = int
    available = bool
    start_time = datetime
    end_time = datetime
    number_of_beds = int
