from database import Base
from sqlalchemy import String,Integer,Boolean,Column,ForeignKey
from sqlalchemy.orm import relationship



class BlogModel(Base):
    __tablename__="blogs"


    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    content=Column(String)
    user_id=Column(Integer,ForeignKey("users.id"))

    user=relationship("UserModel",back_populates="blogs")




class UserModel(Base):
    __tablename__="users"

    
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String)
    email=Column(String)
    password=Column(String)
    isActive=Column(Boolean,default=False)

    blogs=relationship("BlogModel",back_populates="user")

