from database import Base
from sqlalchemy import String,Integer,Boolean,Column



class BlogModel(Base):
    __tablename__="blogs"


    id=Column(Integer,primary_key=True,index=True)
    title=Column(String)
    content=Column(String)