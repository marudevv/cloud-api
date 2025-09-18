import os
from authentication.domain.use_cases import AuthUseCases
from authentication.persistence.redis_token_repo import RedisTokenRepository

class InMemoryUserRepo:
    def __init__(self):
        self.users = {}

    def exists(self, email): return email in self.users
    def create(self, email, password): self.users[email] = password
    def validate(self, email, password): return self.users.get(email) == password

_token_repo = RedisTokenRepository(url=os.getenv("REDIS_URL", "redis://redis:6379/0"))
_user_repo = InMemoryUserRepo()
_auth_uc = AuthUseCases(_token_repo, _user_repo)

def get_auth_uc():
    return _auth_uc
