from fastapi import FastAPI,Depends,HTTPException,status,Response
from schema import BlogSchema,BlogResponseSchema
import models
from models import BlogModel
from database import engine
from sqlalchemy.orm import Session
from database import get_db
from typing import List




models.Base.metadata.create_all(engine)


app=FastAPI()



@app.post("/blog/",status_code=status.HTTP_201_CREATED)
def create_blog(request:BlogSchema,db:Session=Depends(get_db)):
    new_blog=models.BlogModel(title=request.title,content=request.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    if not new_blog:
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail="Not created Blog")
    return new_blog



@app.get("/blog/",status_code=status.HTTP_200_OK,response_model=List[BlogResponseSchema])
def get_blogs_all(db:Session=Depends(get_db)):
    blogs=db.query(models.BlogModel).all()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not found Blogs")
    return blogs




@app.get("/blog/{id}/",status_code=status.HTTP_200_OK,response_model=BlogResponseSchema)
def get_single_blog(id:int,res:Response,db:Session=Depends(get_db)):
    blog=db.query(models.BlogModel).filter(BlogModel.id==id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not vailable in db")
    return blog


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

    

@app.delete("/blog/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_blog(id:int,db:Session=Depends(get_db)):
   blog=db.query(BlogModel).filter(BlogModel.id==id).first()
   if not blog:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Content not found for delete")
   if blog:
       blog.delete(synchronize_session=False)
       db.commit()
       raise HTTPException(status_code=status.HTTP_200_OK,detail=f"Delete Successfully id of {id}")








    
















