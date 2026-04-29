from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException

from app.client import Client, get_client
from app.service import UserService

app = FastAPI()


def get_user_service(
    client: Annotated[Client, Depends(get_client)],
) -> UserService:
    return UserService(client)


@app.get("/users")
def read_users(
    service: Annotated[UserService, Depends(get_user_service)],
    min_age: int | None = None,
    limit: int | None = None,
    offset: int | None = None,
):
    if min_age is not None and min_age < 0:
        raise HTTPException(status_code=400, detail="Min age cannot be negative")

    if limit is not None and limit < 1:
        raise HTTPException(status_code=400, detail="Limit must be greater than zero")

    if offset is not None and offset < 0:
        raise HTTPException(status_code=400, detail="Offset cannot be negative")

    return service.list_users(
        min_age=min_age,
        limit=limit,
        offset=offset,
    )