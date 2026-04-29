import requests
from fastapi import FastAPI, HTTPException, status

app = FastAPI()

USERS_API_URL = "https://dummyjson.com/users"
API_TIMEOUT = 5


@app.get("/users")
def read_users(
    min_age: int | None = None,
    limit: int | None = None,
    offset: int | None = None,
):
    if min_age is not None and min_age < 0:
        raise HTTPException(status_code=400, detail="Min age cannot be negative")
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
        payload = response.json()
    except requests.exceptions.JSONDecodeError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Invalid response from external provider",
        ) from exc

    users = payload.get("users", [])
    out = [
        {
            "id": user.get("id"),
            "full_name": f"{user.get('firstName', '')} {user.get('lastName', '')}".strip(),
            "email": user.get("email"),
            "age": user.get("age"),
            "company": user.get("company", {}).get("name"),
            "country": user.get("address", {}).get("country"),
        }
        for user in users
        if min_age is None or user.get("age") >= min_age
    ]

    if offset is not None:
        if offset > len(users):
            return []
        out = out[offset:]

    if limit is not None:
        return out[:limit]

    return out
