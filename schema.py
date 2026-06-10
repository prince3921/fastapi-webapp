from pydantic import BaseModel


class BlogSchema(BaseModel):
    title:str
    content:str