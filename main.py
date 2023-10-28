from database import get_db,engine
from fastapi import FastAPI,Depends,HTTPException
from sqlalchemy.orm import Session
from model import base
import oauth



app=FastAPI()
app.include_router(oauth.router)

base.metadata.create_all(engine)






# @app.get("/userlogin")
# def user(request:None,db:Session=Depends(get_db)):
#     if request:
#         return {"user":request}
#     else:
#         raise HTTPException(status_code=401,detail="authentication failed")



