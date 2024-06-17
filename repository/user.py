import models
from sqlalchemy.orm import Session


#Peform SQL queries here
def getAll(db: Session):
    users= db.query(models.User).all()
    return users