from typing import Protocol

import requests
from fastapi import HTTPException, status

from app.config import API_TIMEOUT, USERS_API_URL


class Client(Protocol):
    def get_users(self) -> dict: ...


class RequestsClient:
    def get_users(self) -> dict:
        try:
            response = requests.get(USERS_API_URL, timeout=API_TIMEOUT)
            response.raise_for_status()
        except requests.exceptions.Timeout as exc:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Upstream provider timed out",
            ) from exc
        except requests.RequestException as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Failed to fetch users from external provider",
            ) from exc

        try:
            return response.json()
        except requests.exceptions.JSONDecodeError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Invalid response from external provider",
            ) from exc


def get_client() -> Client:
    return RequestsClient()