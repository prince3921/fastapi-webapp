from pydantic import BaseModel


class BlogSchema(BaseModel):
    title:str
    content:str

class BlogResponseSchema(BlogSchema):

    class Config():
        from_attributes = True



class UserSchema(BaseModel):
    username:str
    email:str
    password:str


class UserResponseSchema(UserSchema):
    username:str
    email:str

    class Config():
        from_attributes = True