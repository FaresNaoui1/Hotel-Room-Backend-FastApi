from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import URL_DATABASE

# Set up database engine and session
engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()
