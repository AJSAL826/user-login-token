from model import user
from passlib.context import CryptContext 
from database import get_db
from jose import JWTError,jwt
from datetime import datetime,timedelta
from typing import Annotated
from fastapi import APIRouter,HTTPException,Depends
from pydantic import BaseModel
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from sqlalchemy.orm import Session


router=APIRouter(prefix="/auth",tags=['auth'])
hashing=CryptContext(schemes=['bcrypt'],deprecated='auto')
secretkey='dcmwjhcbhbdcbwbidc2983893ru32092dj283urr823idn8'
algorithm='HS256'

class create_user(BaseModel):
    name:str
    password:str

class token(BaseModel):
    accesstoken:str
    token_type:str

@router.post("/",status_code=status.HTTP_201_CREATED)
def creates_auser(request:create_user,db:Session=Depends(get_db)):
    new_user=user(name=request.name,password=hashing.hash(request.password))
    db.add(new_user)
    db.commit()


#for authenticating and for giving the token 
@router.post("/token",response_model=token)


def create_acess_token(formdata:Annotated[OAuth2PasswordRequestForm,Depends()],db:Session=Depends(get_db)):
    user=check_auth(formdata.username,formdata.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="no user found with this username and password")
    token=token_gen(user.name,user.id,timedelta(minutes=20))
    return {"accesstoken":token,"token_type":"bearer"}




def check_auth(name:str,password:str,db):
    users=db.query(user).filter(user.name==name).first()
    if not users:
        return False
    if not hashing.verify(password, str(users.password)):
        return False
    return users

def token_gen(name:str,id:str,time):
    encode={"name":name,"id":id}
    expire=datetime.utcnow()+time
    encode.update({'exp':expire})
    return jwt.encode(encode,secretkey,algorithm=algorithm)