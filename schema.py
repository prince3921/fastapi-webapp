from pydantic import BaseModel


class BlogSchema(BaseModel):
    title:str
    content:str

class BlogResponseSchema(BlogSchema):

    class Config():
        orm_mode = True