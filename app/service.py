from app.client import Client
from app.mapper import map_users


class UserService:
    def __init__(self, client: Client):
        self.client = client

    def list_users(
        self,
        min_age: int | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[dict]:
        payload = self.client.get_users()
        users = payload.get("users", [])

        users = [
            user
            for user in users
            if min_age is None or user.get("age", 0) >= min_age
        ]

        if offset is not None:
            users = users[offset:]

        if limit is not None:
            users = users[:limit]

        return map_users(users)