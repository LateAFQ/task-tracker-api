from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.api.common.responses import OkResponse
from src.api.v1.auth import Authorization
from src.common import dtos
from src.common.interfaces.mediator import MediatorProtocol

user_router = APIRouter(prefix="/users", tags=["User"])


@user_router.post(
    "",
    status_code=status.HTTP_200_OK,
    response_model=dtos.PublicUser,
)
async def create_user_endpoint(
    body: dtos.CreateUser,
    mediator: Annotated[MediatorProtocol, Depends()],
) -> OkResponse[dtos.PublicUser]:
    return OkResponse(await mediator.send(body))


@user_router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=dtos.PublicUser,
)
async def get_user_by_id_endpoint(
    user: Annotated[dtos.PrivateUser, Authorization()],
    query: Annotated[dtos.SelectUser, Depends(dtos.SelectUser)],
    mediator: Annotated[MediatorProtocol, Depends()],
) -> OkResponse[dtos.PublicUser]:
    return OkResponse(await mediator.send(query))


@user_router.delete(
    "",
    status_code=status.HTTP_200_OK,
    response_model=dtos.PublicUser,
)
async def delete_user_endpoint(
    user: Annotated[dtos.PrivateUser, Authorization()],
    query: Annotated[dtos.DeleteUser, Depends(dtos.DeleteUser)],
    mediator: Annotated[MediatorProtocol, Depends()],
) -> OkResponse[dtos.PublicUser]:
    return OkResponse(await mediator.send(query))


@user_router.patch(
    "",
    status_code=status.HTTP_200_OK,
    response_model=dtos.PublicUser,
)
async def update_user_endpoint(
    user: Annotated[dtos.PrivateUser, Authorization()],
    body: dtos.UpdateUserQuery,
    mediator: Annotated[MediatorProtocol, Depends()],
) -> OkResponse[dtos.PublicUser]:
    return OkResponse(await mediator.send(body))
