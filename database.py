# for creating an engine
from sqlalchemy import create_engine
#This is for mapping
from sqlalchemy.ext.declarative import declarative_base
#talking to the database
#From alchemy
from sqlalchemy.orm import sessionmaker
import database


SQLALCHEMY_DATABASE_URL = "sqlite:///./user.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()  