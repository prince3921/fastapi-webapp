from passlib.hash import pbkdf2_sha256



class PassHashAndVerify():
    
    def PasswordHash(plain_password:str):
        return pbkdf2_sha256.hash(plain_password)
        
    

    def VerifyPassword(plain_password:int,hashed_password):
       return pbkdf2_sha256.verify(plain_password,hashed_password)

