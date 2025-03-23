from fastapi import Depends
from sqlalchemy.orm import Session
from .database.config import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
