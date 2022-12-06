from models.user import User

class Account:
    def __init__(self, jwt, user):
        self.jwt = jwt
        self.user = User(**user)