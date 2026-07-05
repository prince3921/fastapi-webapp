from fastapi import Request,Depends,HTTPException,status
from sqlalchemy.orm import Session
from database import get_db
import jwt
from jwt.exceptions import InvalidTokenError
from models import UserModel

def is_authentication(request:Request,db:Session=Depends(get_db)):
    try:
        # token find through request header through
        token=request.headers.get("authrization")

        print("readCookie",token)

        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are Unauthrized")
        token=token.split(" ")[-1]

        # decode token through jwt
        JWT_SECRET_KEY="ADFGHNDGBNFHVFGB"
        ALGORITHM="HS256"
        data=jwt.decode(token,JWT_SECRET_KEY,ALGORITHM)

        user_id=data.get("user_id")

        # exp_time=data.get("exp")
        # current_time=datetime.now().timestamp()
        # compare_time=current_time > exp_time
        # if compare_time:
        #     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are Unauthrized")
        user=db.query(UserModel).filter(UserModel.id==user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Not Found with the User")

        return user
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are Unauthrized")
