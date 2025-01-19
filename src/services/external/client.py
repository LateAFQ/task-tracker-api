from types import TracebackType
from typing import Any, Optional, Self, Type, TypeVar, Unpack
from urllib.parse import urljoin

from src.api.common.provider.aiohttp import AiohttpProvider, ParamsType
from src.api.common.provider.base import AsyncProvider
from src.services.external.request import Request

RT = TypeVar("RT")


class Client:
    __slots__ = (
        "_provider",
        "_url",
    )

    def __init__(
        self,
        url: str,
        provider: AsyncProvider | None = None,
        *,
        proxy: str | None,
        **options: Unpack[ParamsType],
    ) -> None:
        self._provider = provider or AiohttpProvider(url, proxy, **options)
        self._url = url

    @property
    def url(self) -> str:
        return self._provider.url or self._url

    def endpoint_url(self, endpoint: str) -> str:
        return urljoin(self.url, endpoint)

    async def send(self, request: Request[RT], /, **kwargs: Any) -> RT:
        return await request(self._provider, **kwargs)

    async def __call__(self, request: Request[RT], /, **kwargs: Any) -> RT:
        return await self.send(request, **kwargs)

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        await self._provider.__aexit__(exc_type, exc_value, traceback)
