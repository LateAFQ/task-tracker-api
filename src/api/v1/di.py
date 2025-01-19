from typing import Callable, TypeVar

from fastapi import FastAPI

from src.api.common.cache.redis import get_redis
from src.api.common.security.argon2 import get_argon2_hasher
from src.api.common.security.jwt import JWT
from src.api.v1.handlers import MediatorImpl, setup_mediator
from src.common.interfaces.mediator import MediatorProtocol
from src.core.settings import Settings
from src.database import create_database_factory
from src.database.core.connection import create_sa_engine, create_sa_session_factory
from src.database.core.manager import TransactionManager
from src.database.gateway import DBGateway
from src.services import (
    create_internal_service_gateway_factory,
)
from src.services.internal.gateway import InternalServiceGateway

DependencyType = TypeVar("DependencyType")


def singleton(dependency: DependencyType) -> Callable[[], DependencyType]:
    def singleton_factory() -> DependencyType:
        return dependency

    return singleton_factory


def setup_dependencies(app: FastAPI, settings: Settings) -> None:
    engine = create_sa_engine(
        settings.db.url,
        pool_size=settings.db.connection_pool_size,
        max_overflow=settings.db.connection_max_overflow,
        pool_pre_ping=settings.db.connection_pool_pre_ping,
    )

    redis = get_redis(settings.redis)
    session_factory = create_sa_session_factory(engine)
    database_factory = create_database_factory(TransactionManager, session_factory)
    internal_service_factory = create_internal_service_gateway_factory(
        database_factory, redis
    )
    hasher = get_argon2_hasher()
    jwt = JWT(settings.ciphers)

    app.state.engine = engine
    app.state.redis = redis

    mediator = MediatorImpl()
    setup_mediator(
        mediator,
        internal_gateway=internal_service_factory,
        redis=redis,
        jwt=jwt,
        hasher=hasher,
    )

    app.dependency_overrides[MediatorProtocol] = singleton(mediator)
    app.dependency_overrides[DBGateway] = database_factory
    app.dependency_overrides[InternalServiceGateway] = internal_service_factory
