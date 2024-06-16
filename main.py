from fastapi import FastAPI , Depends
from sqlalchemy.orm import Session
from typing import Optional
import schemas, database , models
from database import engine

app = FastAPI()
models.Base.metadata.create_all(engine)

def get_db():
    db=database.SessionLocal()
    try:
        yield db
    finally:
        db.close()  


@app.post('/')
def addUser(requestBody : schemas.User , db :Session = Depends(get_db)):
    new_user = models.Blog(
        name = requestBody.name,
        email = requestBody.email,
        password =requestBody.password
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
