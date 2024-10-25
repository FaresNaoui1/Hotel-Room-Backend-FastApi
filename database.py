from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Update the URL_DATABASE to use MySQL
URL_DATABASE = 'mysql+pymysql://root:12345@localhost:3306/hotel'

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()

# Testing the connection
try:
    with engine.connect() as connection:
        print("Connection to the MySQL database successful!")
except Exception as e:
    print(f"An error occurred: {e}")
