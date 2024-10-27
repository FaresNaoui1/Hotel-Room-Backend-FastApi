from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database URL should be set up as an environment variable for security.
# Example: export DATABASE_URL="mysql+pymysql://root:12345@localhost:3306/hotel"
DATABASE_URL = "mysql+pymysql://root:12345@localhost:3306/hotel"  # Change this in production

# Set up database engine
engine = create_engine(DATABASE_URL, connect_args={"charset": "utf8mb4"})

# Create a configured "Session" class
SessionLocal = sessionmaker(autoflush=False, bind=engine)

# Create a Base class for declarative models
Base = declarative_base()
