from sqlalchemy import Column,String,Integer
from sqlalchemy.orm import declarative_base


base=declarative_base()


class user(base):
    __tablename__="Userlogin"
    id=Column(Integer,primary_key=True)
    name=Column(String)
    password=Column(String)