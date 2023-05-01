from pydantic import BaseModel, EmailStr


class User(BaseModel):
    """ 
        The model will be used 
        as response model 
        where we do not want to interact 
        with the password, 
        reducing the amount of work to be done.
    """
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "fastapi@mymail.com",
                "password": "strong!!!",
            }
        }


class UserSignIn(BaseModel):
    """
        This model will be used 
        as the data type 
        when registering a new user.
    """
    email: EmailStr
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "fastapi@mymail.com",
                "password": "strong!!!"
            }
        }