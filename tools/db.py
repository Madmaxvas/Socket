from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, email: str, username: str, name: str,password: str):
        self.id = username
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.authenticated = False

    def is_authenticated(self):
        return self.authenticated