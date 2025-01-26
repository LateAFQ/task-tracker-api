from typing import Callable

from src.api.common.cache.redis import RedisCache
from src.database.gateway import DBGateway

from .internal.gateway import InternalServiceGateway

InternalServiceGatewayFactory = Callable[[], InternalServiceGateway]


def create_internal_service_gateway_factory(
    database: Callable[[], DBGateway],
    redis: RedisCache,
) -> InternalServiceGatewayFactory:
    def _create_instance() -> InternalServiceGateway:
        return InternalServiceGateway(database(), redis)

    return _create_instance



__all__ = (
    "InternalServiceGateway",
    "ExternalServiceGateway",
)
