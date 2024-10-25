from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from Classes.User import User  # Import User model from Classes

from database import SessionLocal
from pydantic_model_user import UserBase, UserCreate

# JWT configuration
SECRET_KEY = "4e1e76881775c98ba7ead8b291c2f434b8bc3f8365635159993ab9c5b3045ecb2ce52c9539fae57f5113e1c2ecab6492f5f28f2670d2b30632c32ccd932934b9895e629d6865255bc90e16794bf22bb96482bcd33bb8ae7334ad77688d6f9a08eaf383f7b946d7a50db951e0a95a1f502434363040aa92196bbdd668e420516221ead35cee1d24f40b968789d781e7200d1e9cd1be1c466294b6e2771d8ea8f1b322c8ba76ae313f77876b9270eadd40061462a8873eedc000ba224eca0ba3bddfe8ac218bfc01dd84c064db1eab373766576a8f0986ffd9685d4cf9e4862aad256078fea88545a43d6129c5ea656fa49533eaa6ad39dab8559f5ea589f05e56"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing configuration
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# FastAPI router
router = APIRouter()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# JWT utility functions
def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=username)
    if user is None:
        raise credentials_exception
    return user

# Authentication endpoint
@router.post("/token", response_model=dict)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# User registration endpoint
@router.post("/users/", response_model=UserBase, status_code=status.HTTP_201_CREATED)
async def create_user(new_user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(
        username=new_user.username,
        email=new_user.email,
        hashed_password=get_password_hash(new_user.password)
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return db_user

# Get user by ID
@router.get("/users/{user_id}", response_model=UserBase, status_code=200)
async def read_user(user_id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Delete user by ID
@router.delete("/users/{user_id}", status_code=status.HTTP_202_ACCEPTED)
async def delete_user(user_id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": f"User {user_id} has been deleted"}

# Get all users endpoint
@router.get("/users", response_model=List[UserBase], status_code=200)
async def get_all_users(db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    users = db.query(User).all()
    return users
