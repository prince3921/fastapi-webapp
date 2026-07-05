from pydantic import BaseModel
from typing import List,Optional

class BlogSchema(BaseModel):
    title:str
    content:str

class BlogUpdateSchema(BaseModel):
    title:Optional[str]=None
    content:Optional[str]=None


# user Schema

class LoginSchema(BaseModel):
    email:str
    password:str


class SignUpSchema(LoginSchema):
    username:str







# class BlogResponseSchema(UserSchemaRead):
#     id:int
#     title:str
#     content:str
#     # user_id:UserSchemaRead

#     class Config():
#         from_attributes = True



