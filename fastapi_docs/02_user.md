
## Authentication
Model
Schema
helper
db

### Create User(Signup and HashingPassword) 
- UserModel create
- import Column,Interger,Boolean,DateTime,String from sqlalchemy
- create class UserModel and inherit Base
- __tablename__="users" is a table name define
- table_field define
- id is Interger,primary_key is true
- username String,nullable is false
- name String
- email String 
- hash_password is string
- mobile(as a task)

- UserSchema define for response sending on data control
- token generate through jwt
- install pyjwt using pip
- password hash using passlib or "pwdlib[argon2]"
- install using pip through passlib,pwdlib[argon2]
- PasswordHash impot from pwdlib
- PasswordHash through plain_password and get hashedPassword
- find user by username , password through
- user is exist raise HTTPException All ready User exist
- user not found then
- plain password hashed using pwdlib
- before creating user password is replace hashPassword in UserModel
- and create user
- db through add user
- db through commit
- db through refrash user
- return user_data

- improve reoute and data control
- status_code
- response_model
