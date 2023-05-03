from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto')

class HashPassword:

    def create_hash(self, password: str):
        """
            The method takes a string and returns a hashed value.
        """
        return pwd_context.hash(password)

    def verify_hash(self, plain_password: str, hashed_password: str):
        """
            Takes a plain password 
            and a hashed password 
            and compares them. 
            The function returns a Boolean value 
            indicating whether the values passed 
            are the same or not.
        """
        return pwd_context.verify(plain_password, hashed_password)
    