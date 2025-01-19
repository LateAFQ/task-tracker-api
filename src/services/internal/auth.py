import uuid
from typing import Literal

from fastapi import Request
from fastapi.concurrency import run_in_threadpool
from fastapi.security.utils import get_authorization_scheme_param

from src.api.common.cache.redis import RedisCache
from src.api.common.security.jwt import JWT
from src.common import dtos
from src.common.exceptions import ForbiddenError

TokenType = Literal["access", "refresh"]


class AuthService:
    __slots__ = ("_jwt", "_cache")

    def __init__(self, jwt: JWT, cache: RedisCache) -> None:
        self._jwt = jwt
        self._cache = cache

    async def verify_refresh(
        self,
        body: dtos.Fingerprint,
        refresh_token: str,
        user: dtos.PrivateUser,
    ) -> dtos.TokensExpire:
        await self.verify_token(refresh_token, "refresh")
        token_pairs = await self._cache.get_list(str(user.uuid))
        verified = None
        for pair in token_pairs:
            data = pair.split("::")
            if len(data) < 2:
                await self._cache.delete(str(user.uuid))
                raise ForbiddenError(
                    "Broken separator, try to login again. Token is not valid anymore"
                )
            fp, cached_token, *_ = data
            if fp == body.fingerprint and cached_token == refresh_token:
                verified = pair
                break

        if not verified:
            await self._cache.delete(str(user.uuid))
            raise ForbiddenError("Token is not valid anymore")

        await self._cache.pop(str(user.uuid), verified)
        _, access = await run_in_threadpool(
            self._jwt.create, typ="access", sub=str(user.uuid)
        )
        expire, refresh = await run_in_threadpool(
            self._jwt.create, typ="refresh", sub=str(user.uuid)
        )
        await self._cache.set_list(
            str(user.uuid), f"{body.fingerprint}::{refresh.token}"
        )

        return dtos.TokensExpire(
            refresh_expire=expire,
            tokens=dtos.Tokens(access=access.token, refresh=refresh.token),
        )

    async def invalidate_refresh(
        self,
        refresh_token: str,
        user: dtos.PrivateUser,
    ) -> dtos.Status:
        await self.verify_token(refresh_token, "refresh")
        token_pairs = await self._cache.get_list(str(user.uuid))
        for pair in token_pairs:
            data = pair.split("::")
            if len(data) < 2:
                await self._cache.delete(str(user.uuid))
                break
            _, cached_token, *_ = data
            if cached_token == refresh_token:
                await self._cache.pop(str(user.uuid), pair)
                break

        return dtos.Status(ok=True)

    async def verify_token(
        self,
        token: str,
        token_type: TokenType,
    ) -> uuid.UUID:
        payload = await run_in_threadpool(self._jwt.verify_token, token)
        actual_token_type = payload.get("type")
        user_id = payload.get("sub")

        if actual_token_type != token_type:
            raise ForbiddenError("Invalid token")

        return uuid.UUID(user_id)

    def _get_token(self, request: Request) -> str:
        authorization = request.headers.get("Authorization")
        scheme, token = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and token):
            raise ForbiddenError("Not authenticated")
        if scheme.lower() != "bearer":
            raise ForbiddenError("Invalid authentication credentials")

        return token
