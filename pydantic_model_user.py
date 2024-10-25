from pydantic import BaseModel, EmailStr, ConfigDict

class UserBase(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_admin: bool

    # Config for mapping ORM objects to Pydantic model in FastAPI
    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str  # Only required for creation, so placed here
