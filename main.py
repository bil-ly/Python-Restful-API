from fastapi import FastAPI , Depends , status , Response , HTTPException
from sqlalchemy.orm import Session
from typing import Optional ,List
import schemas, database , models , hashing
from database import engine
from routers import user 


app = FastAPI()
models.Base.metadata.create_all(engine)

def get_db():
    db=database.SessionLocal()
    try:
        yield db
    finally:
        db.close() 

#app.include_router(user.router)         


@app.post('/users', status_code=status.HTTP_201_CREATED , response_model=schemas.ShowUser, tags=["User"])
def addUser(requestBody : schemas.User , db :Session = Depends(get_db)):
    new_user = models.User(
        name = requestBody.name,
        email = requestBody.email,
        password =hashing.Hash.hash_pwd(requestBody.password)
        )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get('/users', response_model=List[schemas.ShowUser], tags=["User"])
def getAll(db:Session=Depends(get_db)):
    users= db.query(models.User).all()
    return users

@app.get('/users/{id}' , status_code=status.HTTP_200_OK , response_model=schemas.ShowUser, tags=["User"])
def getUser(id ,response : Response ,db:Session=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id ==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f'User with id{id} does not exist')
        
    return user

@app.delete('/users/{id}' , status_code=status.HTTP_204_NO_CONTENT, tags=["User"])
def deleteUser(id,db:Session=Depends(get_db)):
    user= db.query(models.User).filter(models.User.id == id).delete()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail =f'User with id{id} does not exist')
    db.commit()
    return f"Blog with ID{id} has been deleted"

@app.put('/users/{id}', tags=["User"])
def updateUser(id,requestBody :schemas.User,db:Session = Depends(get_db)):
    db.query(models.User).filter(models.User.id == id).update({
        "name": requestBody.name
    })
    db.commit()
    return f"Blog with ID {id} is updated"

