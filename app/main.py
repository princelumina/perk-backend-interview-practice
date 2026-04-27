from http.client import HTTPException

import requests
from fastapi import FastAPI

app = FastAPI()

USERS_API_URL = "https://dummyjson.com/users"

@app.get("/users")
def read_users():
    try:
        response = requests.get(USERS_API_URL, timeout=5)
        response.raise_for_status()
    except requests.RequestException as exc:
        raise HTTPException(
            status_code=502,
            detail="Failed to fetch users from external provider",
        ) from exc
    payload = response.json()
    users = payload.get("users", [])
    return [
        {
            "id": user.get("id"),
            "full_name": f"{user.get('firstName', '')} {user.get('lastName', '')}".strip(),
            "email": user.get("email"),
            "age": user.get("age"),
            "company": user.get("company", {}).get("name"),
            "country": user.get("address", {}).get("country"),
        }
        for user in users
    ]