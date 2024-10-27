from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import os

URL_DATABASE = os.getenv("DATABASE_URL")  # Set DATABASE_URL in Render


# Set up database engine
engine = create_engine(URL_DATABASE, connect_args={"charset": "utf8mb4"})

# Create a configured "Session" class
SessionLocal = sessionmaker(autoflush=False, bind=engine)

# Create a Base class for declarative models
Base = declarative_base()
