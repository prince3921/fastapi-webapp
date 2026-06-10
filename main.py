from fastapi import FastAPI,Depends,HTTPException,status,Response
from schema import BlogSchema,BlogResponseSchema,UserSchema,UserResponseSchema
import models
from models import BlogModel,UserModel
from database import engine
from sqlalchemy.orm import Session
from database import get_db
from typing import List




models.Base.metadata.create_all(engine)


app=FastAPI()


# blog create

@app.post("/blog/",status_code=status.HTTP_201_CREATED)
def create_blog(request:BlogSchema,db:Session=Depends(get_db)):
    new_blog=models.BlogModel(title=request.title,content=request.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    if not new_blog:
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail="Not created Blog")
    return new_blog

# read all blogs

@app.get("/blog/",status_code=status.HTTP_200_OK,response_model=List[BlogResponseSchema])
def get_blogs_all(db:Session=Depends(get_db)):
    blogs=db.query(models.BlogModel).all()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not found Blogs")
    return blogs


# read single blog

@app.get("/blog/{id}/",status_code=status.HTTP_200_OK,response_model=BlogResponseSchema)
def get_single_blog(id:int,res:Response,db:Session=Depends(get_db)):
    blog=db.query(models.BlogModel).filter(BlogModel.id==id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not vailable in db")
    return blog


# update blog

@app.put("/blog/{id}",status_code=status.HTTP_202_ACCEPTED)
def update_blog(id:int,request:BlogSchema,db:Session=Depends(get_db)):
   data=request.model_dump()
#    call database and get user
   blog= db.query(models.BlogModel).filter(models.BlogModel.id==id).first()
#  user not found
   if not blog:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not Update with id {id} Successfully")
   if blog:
    blog.update(data)
    db.commit()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail={
        "status":"update successfully",
        "data":data
    })

# delete blog

@app.delete("/blog/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id:int,db:Session=Depends(get_db)):
   blog=db.query(BlogModel).filter(BlogModel.id==id).first()
   if not blog:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Content not found for delete")
   if blog:
       blog.delete(synchronize_session=False)
       db.commit()
       raise HTTPException(status_code=status.HTTP_200_OK,detail=f"Delete Successfully id of {id}")






# user create

@app.post("/users/",status_code=status.HTTP_201_CREATED)
def create_user(request:UserSchema,db:Session=Depends(get_db)):

    # data=request.model_dump()

    new_user=UserModel(username=request.username,email=request.email,password=request.password)
    # user find by email,username
    
    user=db.query(UserModel).filter(UserModel.email==new_user.email).first()


    if not user:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    raise HTTPException(status_code=status.HTTP_208_ALREADY_REPORTED,detail={"message":"User Allready Exist"})

    
    
# get current user

@app.get("/users/{id}",response_model=UserResponseSchema)
def get_single_user(id:int,db:Session=Depends(get_db)):
    user=db.query(UserModel).filter(UserModel.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message":"User Not Found","data":False})
    return user



# delete user

@app.delete("/users/{id}",status_code=status.HTTP_200_OK)
def dlete_user(id:int,db:Session=Depends(get_db)):
    user=db.query(UserModel).filter(UserModel.id==id).delete(synchronize_session=False)
    db.commit()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message":"User Not Found","data":False})
    
    raise HTTPException(status_code=status.HTTP_200_OK,detail={"message":"User Delete Successfully","data":True})    
    


        
    
    


       
















