import uuid
from datetime import timedelta

class AuthUseCases:
    def __init__(self, token_repo, user_repo):
        self.token_repo = token_repo
        self.user_repo = user_repo

    def register(self, email, password):
        if self.user_repo.exists(email):
            raise ValueError("User already exists")
        self.user_repo.create(email, password)

    def login(self, email, password):
        if not self.user_repo.validate(email, password):
            raise ValueError("Invalid credentials")
        token = str(uuid.uuid4())
        self.token_repo.save(token, {"email": email}, ttl=timedelta(hours=12))
        return token

    def logout(self, token):
        self.token_repo.delete(token)

    def introspect(self, token):
        data = self.token_repo.get(token)
        if not data:
            raise ValueError("Invalid token")
        return {"active": True, "user": data}

    def validate_token(self, token: str) -> bool:
        return self.token_repo.get(token) is not None
