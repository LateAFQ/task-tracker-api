from typing import Annotated

from pydantic import Field

from src.common.dtos.base import DTO


class AuthorizeByCode(DTO):
    code: Annotated[
        str,
        Field(
            description="Код авторизации",
            example="4f102644-5b0c-44be-8a02-71b4c29a6600",
        ),
    ]
