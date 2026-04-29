def map_user(user: dict):
    return {
        "id": user.get("id"),
        "full_name": f"{user.get('firstName', '')} {user.get('lastName', '')}".strip(),
        "email": user.get("email"),
        "age": user.get("age", 0),
        "company": user.get("company", {}).get("name"),
        "country": user.get("address", {}).get("country"),
    }


def map_users(users: list):
    return [map_user(user) for user in users]