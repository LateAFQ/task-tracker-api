from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.api.common.docs import ForbiddenError, UnAuthorizedError
from src.api.common.responses import OkResponse
from src.api.v1.auth import Authorization
from src.api.v1.handlers import auth
from src.api.v1.handlers.auth.login import LoginQuery
from src.common import dtos
from src.common.interfaces.mediator import MediatorProtocol

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.post(
    "/login",
    status_code=status.HTTP_200_OK,
    response_model=dtos.Token,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ForbiddenError},
        status.HTTP_401_UNAUTHORIZED: {"model": UnAuthorizedError},
    },
)
async def login_by_code_endpoint(
    body: LoginQuery,
    mediator: Annotated[MediatorProtocol, Depends()],
) -> OkResponse[dtos.Token]:
    result = await mediator.send(body)
    response = OkResponse(dtos.Token(token=result.tokens.access))
    response.set_cookie(
        "refresh_token",
        value=result.tokens.refresh,
        expires=result.refresh_expire,
        httponly=True,
        # secure=True,
        samesite="lax",
    )
    return response


@auth_router.post(
    "/refresh",
    status_code=status.HTTP_200_OK,
    response_model=dtos.Token,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": UnAuthorizedError},
        status.HTTP_403_FORBIDDEN: {"model": ForbiddenError},
    },
)
async def refresh_endpoint(
    body: dtos.Fingerprint,
    mediator: Annotated[MediatorProtocol, Depends()],
    user: Annotated[dtos.PrivateUser, Depends(Authorization(only_refresh=True))],
) -> OkResponse[dtos.Token]:
    result = await mediator.send(auth.RefresTokenQuery(data=body, user=user))
    response = OkResponse(dtos.Token(token=result.tokens.access))
    response.set_cookie(
        "refresh_token",
        value=result.tokens.refresh,
        expires=result.refresh_expire,
        httponly=True,
        # secure=True,
        samesite="lax",
    )

    return response


@auth_router.post(
    "/logout",
    status_code=status.HTTP_200_OK,
    response_model=dtos.Status,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": UnAuthorizedError},
        status.HTTP_403_FORBIDDEN: {"model": ForbiddenError},
    },
)
async def logout_endpoint(
    mediator: Annotated[MediatorProtocol, Depends()],
    user: Annotated[dtos.PrivateUser, Depends(Authorization())],
) -> OkResponse[dtos.Status]:
    result = await mediator.send(auth.LogoutQuery(user=user))
    response = OkResponse(result)
    response.delete_cookie("refresh_token")

    return response
