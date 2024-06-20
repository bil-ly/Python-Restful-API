from passlib.context import CryptContext



pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated = "auto")

class Hash():
    def hash_pwd(password : str):
        return pwd_cxt.hash(password)
    
    # verifying the users password with the hash , by comparing the
    def verify(plain_pwd , hashed_pwd):
        return pwd_cxt.verify(plain_pwd ,hashed_pwd)
    

        