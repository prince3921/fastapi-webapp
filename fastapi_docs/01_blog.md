## Blog Update 
- accpet data, body type blogSchema,blog_id type integer,db type Session
- Session import form sqlalchemy.orm
- ask db.query accept blogModel
- check through blog_id through blog find success then retutn comming data
- not blog find then raise HTTPExeption
------
```py
    # update logic (required all value)
    blog.title=body.title
    blog.discription=body.discription
  
   # update logic (required individual value)
   body=body.model_dump()
   for field,value in body.items():
       setattr(blog,field,value)
   
```

- add in db in comming blog
- commit db
- db through refresh
- return success message


## Delete Blog
- accept data in parameter in
- blog_id is type of int
- db is type of Session
- blog_id through find blog
- if not blog then raise HTTPException
- db through blog delete
- db through commit
- return success message


## improvement endpoint route in
- response_model include from blogSchema
- response_model to control on response_Schema which element not return not extra value return like password
- blogSchema inherit by pydentic BaseModel
- success route then status_code=status.HTTP_...
- status import from fastapi
- delete route no_content return



