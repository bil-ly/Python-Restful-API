import models
from sqlalchemy.orm import Session
def getAll(db: Session):
    users= db.query(models.User).all()
    return users

#Peform SQL queries here
