from typing import List, Optional
from pydantic import BaseModel

class User(BaseModel):
    name:str
    email:str
    password:str

# Response
class ShowUser(BaseModel):
    name:str
    email:str
    class Config():
        orm_mode = True

# For Login
class Login(BaseModel):
    username:str
    password:str        