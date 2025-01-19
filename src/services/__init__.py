from typing import Callable

from src.api.common.cache.redis import RedisCache
from src.core.settings import Settings
from src.database.gateway import DBGateway

from .external.gateway import ExternalServiceGateway
from .internal.gateway import InternalServiceGateway

InternalServiceGatewayFactory = Callable[[], InternalServiceGateway]
ExternalServiceGatewayFactory = Callable[[], ExternalServiceGateway]


def create_internal_service_gateway_factory(
    database: Callable[[], DBGateway],
    redis: RedisCache,
) -> InternalServiceGatewayFactory:
    def _create_instance() -> InternalServiceGateway:
        return InternalServiceGateway(database(), redis)

    return _create_instance


def create_external_service_gateway_factory(
    database: Callable[[], DBGateway],
    settings: Settings,
) -> ExternalServiceGatewayFactory:
    def _create_instance() -> ExternalServiceGateway:
        return ExternalServiceGateway(settings, database())

    return _create_instance


__all__ = (
    "InternalServiceGateway",
    "service_gateway_factory",
    "ExternalServiceGateway",
)
