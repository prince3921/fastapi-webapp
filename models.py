from database import Base
from sqlalchemy import String,Integer,Boolean,Column



class BlogModel(Base):
    __tablename__="blogs"


    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    content=Column(String)




class UserModel(Base):
    __tablename__="users"

    
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String)
    email=Column(String)
    password=Column(String)
    isActive=Column(Boolean,default=False)