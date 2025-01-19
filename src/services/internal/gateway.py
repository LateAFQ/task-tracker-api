from src.api.common.cache.redis import RedisCache
from src.api.common.security.jwt import JWT
from src.common.interfaces.gateway import BaseGateway
from src.database import DBGateway
from src.services.internal.auth import AuthService
from src.services.internal.role import RoleService
from src.services.internal.user import UserService


class InternalServiceGateway(BaseGateway):
    __slots__ = ("database", "redis", "_settings")

    def __init__(
        self,
        database: DBGateway,
        redis: RedisCache,
    ) -> None:
        self.database = database
        self.redis = redis
        super().__init__(database)

    def user(self) -> UserService:
        return UserService(self.database.user())

    def auth(self, jwt: JWT, cache: RedisCache) -> AuthService:
        return AuthService(jwt, cache)

    def role(self) -> RoleService:
        return RoleService(self.database.role())
