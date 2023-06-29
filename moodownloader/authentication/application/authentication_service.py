from ..domain.authenticator import Authenticator


class AuthenticationService:
    def __init__(self, authenticator: Authenticator) -> None:
        self.authenticator = authenticator
    
    def authenticate_user(self) -> bool:
        return self.authenticator.authenticate()