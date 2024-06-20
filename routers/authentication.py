from fastapi import APIRouter , Depends , HTTPException , Response , status
import schemas , database , models , hashing
from sqlalchemy.orm import Session

router = APIRouter(tags=["Authentication"])

@router.post('/login')
def login(requestBody:schemas.Login , db:Session =Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == requestBody.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Invalid Credentials")
    
    if not hashing.Hash.verify(requestBody.password , user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="Invalid Credentials")

    return user