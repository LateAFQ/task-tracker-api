import abc
from typing import Any, Generic, TypeVar

from src.api.common.provider.base import AsyncProvider
from src.api.common.provider.response import Response
from src.api.common.provider.types import RequestMethodType
from src.common.interfaces.handler import Handler

ProviderType = TypeVar("ProviderType")
ResultType = TypeVar("ResultType")


class Request(Handler, Generic[ResultType]):
    async def __call__(self, provider: AsyncProvider, **kwargs: Any) -> ResultType:
        return await self.handle(provider, **kwargs)

    @abc.abstractmethod
    async def handle(self, provider: AsyncProvider, **kwargs: Any) -> ResultType:
        raise NotImplementedError


class BasicRequest(Request[Response]):
    __slots__ = ("_method", "_data", "_url_or_endpoint")

    def __init__(self, method: RequestMethodType, url_or_endpoint: str) -> None:
        self._method = method
        self._url_or_endpoint = url_or_endpoint

    async def handle(self, provider: AsyncProvider, **kwargs: Any) -> Response:
        return await provider(
            self._method, url_or_endpoint=self._url_or_endpoint, **kwargs
        )
