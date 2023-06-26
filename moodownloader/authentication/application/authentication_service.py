from moodownloader.authentication.domain import User, Authenticator


class AuthenticationService:
    def __init__(self, authenticator: Authenticator) -> None:
        self.authenticator = authenticator
    
    def authenticate_user(self, user: User) -> bool:
        self.authenticator.username = user.username
        self.authenticator.password = user.password
        return self.authenticator.authenticate()