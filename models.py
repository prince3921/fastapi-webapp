from database import Base
from sqlalchemy import String,Integer,Boolean,Column,ForeignKey
from sqlalchemy.orm import relationship



# in process for relationship with models



class BlogModel(Base):
    __tablename__="blogs"


    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    content=Column(String)
    user_id=Column(Integer,ForeignKey("users.id",ondelete="CASCADE"))





class UserModel(Base):
    __tablename__="users"

    
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String)
    email=Column(String)
    password=Column(String)
    is_validate=Column(Boolean,default=False)
    isActive=Column(Boolean,default=False)
    


