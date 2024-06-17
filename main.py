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


@app.post('/users')
def addUser(requestBody : schemas.User , db :Session = Depends(get_db)):
    new_user = models.User(
        name = requestBody.name,
        email = requestBody.email,
        password =requestBody.password
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get('/users')
def getAll(db:Session=Depends(get_db)):
    users= db.query(models.User).all()
    return users

@app.get('/users/{id}')
def getUser(id , db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id ==id).first()
    return user

@app.delete('/users/{id}')
def deleteUser(id,db:Session=Depends(get_db)):
    user= db.query(models.User).filter(models.User.id == id).delete()
    db.commit()
    return f"Blog with ID{id} has been deleted"

@app.put('/users/{id}')
def updateUser(id,requestBody :schemas.User,db:Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id == id).update({
        "name": requestBody.name
    })
    db.commit()
    return f"Blog with ID {id} is updated"
