from fastapi import FastAPI,Depends,HTTPException,status,Cookie,Response
from schema import BlogSchema,SignUpSchema,LoginSchema,BlogUpdateSchema
import models
from models import BlogModel,UserModel
from database import engine
from sqlalchemy.orm import Session
from database import get_db
# from typing import List
from utils.utils import PassHashAndVerify
import jwt
from datetime import datetime,timedelta
# from jwt.exceptions import InvalidTokenError
from utils.auth_potected import is_authentication


models.Base.metadata.create_all(engine)

# tags feature to saperate route
user_tag="User"
blog_tag="Blog"


app=FastAPI()


# blog create
# response model user_id add in blogSchmaResponse in field

@app.post("/blog/",status_code=status.HTTP_201_CREATED,tags=[blog_tag])
def create_blog(request:BlogSchema,db:Session=Depends(get_db),user:UserModel=Depends(is_authentication)):

    new_blog=models.BlogModel(title=request.title,content=request.content,user_id=user.id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    if not new_blog:
        raise HTTPException(status_code=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION,detail="Not created Blog")
    return new_blog

# read all blogs

@app.get("/blog/",status_code=status.HTTP_200_OK,tags=[blog_tag])
def get_blogs_all(db:Session=Depends(get_db),user:UserModel=Depends(is_authentication)):
    blogs=db.query(models.BlogModel).all()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not found Blogs")
    return blogs


# read single blog

@app.get("/blog/{id}/",status_code=status.HTTP_200_OK,tags=[blog_tag])
def get_single_blog(id:int,db:Session=Depends(get_db),user:UserModel=Depends(is_authentication)):
    blog=db.query(models.BlogModel).filter(BlogModel.id==id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with the id {id} is not vailable in db")
    return blog


# update blog(revisit)

@app.put("/blog/{id}",status_code=status.HTTP_202_ACCEPTED,tags=[blog_tag])
def update_blog(id:int,request:BlogUpdateSchema,db:Session=Depends(get_db),user:UserModel=Depends(is_authentication)):
   data=request.model_dump()
      
#    call database and get user
   blog= db.query(models.BlogModel).filter(models.BlogModel.id==id).update(request,synchronize_session=False)

    # if request.content is not None:
    #     blog.content=request.content

    # if request.title is not None:
    #     blog.title=request.title


    # db.add(blog)
    # db.commit()
    # db.refresh(blog)     
#  user not found
   if not blog:
       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"Not Update with id {id}")
       
       
   raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail={"status":"update successfully","data":data
    })
    
        
        

# delete blog

@app.delete("/blog/{id}",status_code=status.HTTP_204_NO_CONTENT,tags=[blog_tag])
def delete_blog(id:int,db:Session=Depends(get_db),user:UserModel=Depends(is_authentication)):
   blog=db.query(BlogModel).filter(BlogModel.id==id).first()
   if not blog:
       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Content not found for delete")
   if blog:
       db.delete(blog)
       db.commit()
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Delete Successfully id of {id}")






# user create
# response model improve
@app.post("/users/register/",status_code=status.HTTP_201_CREATED,tags=[user_tag])
def create_user(request:SignUpSchema,db:Session=Depends(get_db)):

    # data=request.model_dump()

    # find user bases of username and password
    user_find_by_username=db.query(UserModel).filter(UserModel.username==request.username).first()

    print("user_username",user_find_by_username)

    if user_find_by_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User Exist using by username")

    user_find_by_email=db.query(UserModel).filter(UserModel.email==request.email).first()
    print(user_find_by_email)

    print("user_email",user_find_by_email)


    if user_find_by_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User Exist using by email")

    if user_find_by_username or user_find_by_email:
        raise HTTPException(status_code=status.HTTP_417_EXPECTATION_FAILED,detail="User Allready exist")
    else:
        # password incrypt
        hashedPassword=PassHashAndVerify.PasswordHash(request.password)

        print("hashed_password",hashedPassword)

        if hashedPassword:
            new_user=UserModel(username=request.username,email=request.email,password=hashedPassword)
            # user find by email,username
            user=db.query(UserModel).filter(UserModel.email==new_user.email).first()


            if not user:
                db.add(new_user)
                db.commit()
                db.refresh(new_user)
                return {"user":new_user,"message":"User Successfully created"}
        else:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Password encode issue")    
    

# user login
@app.post("/users/login",status_code=status.HTTP_201_CREATED)
async def login_user(request:LoginSchema,response:Response,db:Session=Depends(get_db)):
    
    # find by email
    user=db.query(UserModel).filter(UserModel.email==request.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="your email is wrong")

    # if user exist then verify password
    is_verify_user=  PassHashAndVerify.VerifyPassword(request.password,user.password)

    if not is_verify_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Login Credential wrong")
    
    EXPIRE_TIME_MINUTE=30
    exp_time=datetime.now() + timedelta(days=EXPIRE_TIME_MINUTE)
    
    data={"user_id":user.id,"email":user.email,"exp":exp_time.timestamp()}
    JWT_SECRET_KEY="ADFGHNDGBNFHVFGB"
    ALGORITHM="HS256"
    

    token= jwt.encode(data,JWT_SECRET_KEY,ALGORITHM)

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="JWT Token Generation Error")

    # print({"token":token})

    # expire=datetime.now()+timedelta(days=7)

    # set cookie 
    response.set_cookie(
        key="token",
        value=token,
        expires=86400,
        secure=True,
        httponly=True,
        # samesite=["strict"]
    ),

    return {"message":"Login Success","data":user}




    




    
# get current user

@app.get("/users/getcurrentuser/",tags=[user_tag])
def get_current_user(db:Session=Depends(get_db),user:UserModel=Depends(is_authentication)):
    userres=db.query(UserModel).filter(UserModel.id==user.id).first()
    if not userres:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message":"You are not Authenticate","data":False})
    return userres



@app.put("/users/upadte",status_code=status.HTTP_201_CREATED)
def update_user():
    pass





# delete user

@app.delete("/users/delete/",status_code=status.HTTP_200_OK,tags=[user_tag])
def delete_user(db:Session=Depends(get_db),user:UserModel=Depends(is_authentication)):
    userres=db.query(UserModel).filter(UserModel.id==user.id).delete(synchronize_session=False)
    db.commit()

    if not userres:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"message":"You are not authenticated","success":False})
    raise HTTPException(status_code=status.HTTP_200_OK,detail={"message":"User Delete Successfully","success":True})    
    



    
    


       
















