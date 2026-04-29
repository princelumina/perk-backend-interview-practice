import pytest
from fastapi.testclient import TestClient

from app.client import Client
from app.main import app, get_user_service
from app.service import UserService


class MockClient(Client):
    def get_users(self) -> dict:
        return {
            "users": [
                {
                    "id": 1,
                    "firstName": "Emily",
                    "lastName": "Johnson",
                    "email": "emily@example.com",
                    "age": 30,
                    "company": {"name": "Acme"},
                    "address": {"country": "United States"},
                },
                {
                    "id": 2,
                    "firstName": "John",
                    "lastName": "Smith",
                    "email": "john@example.com",
                    "age": 40,
                    "company": {"name": "Globex"},
                    "address": {"country": "Germany"},
                },
                {
                    "id": 3,
                    "firstName": "Sara",
                    "lastName": "Miller",
                    "email": "sara@example.com",
                    "age": 50,
                    "company": {"name": "Initech"},
                    "address": {"country": "Spain"},
                },
            ]
        }


@pytest.fixture
def test_client():
    def override_user_service() -> UserService:
        return UserService(MockClient())

    app.dependency_overrides[get_user_service] = override_user_service

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()


def test_get_users_returns_mapped_users(test_client):
    response = test_client.get("/users")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "full_name": "Emily Johnson",
            "email": "emily@example.com",
            "age": 30,
            "company": "Acme",
            "country": "United States",
        },
        {
            "id": 2,
            "full_name": "John Smith",
            "email": "john@example.com",
            "age": 40,
            "company": "Globex",
            "country": "Germany",
        },
        {
            "id": 3,
            "full_name": "Sara Miller",
            "email": "sara@example.com",
            "age": 50,
            "company": "Initech",
            "country": "Spain",
        },
    ]


def test_get_users_filters_by_min_age(test_client):
    response = test_client.get("/users?min_age=35")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 2,
            "full_name": "John Smith",
            "email": "john@example.com",
            "age": 40,
            "company": "Globex",
            "country": "Germany",
        },
        {
            "id": 3,
            "full_name": "Sara Miller",
            "email": "sara@example.com",
            "age": 50,
            "company": "Initech",
            "country": "Spain",
        },
    ]


def test_get_users_paginates_results(test_client):
    response = test_client.get("/users?limit=1&offset=1")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 2,
            "full_name": "John Smith",
            "email": "john@example.com",
            "age": 40,
            "company": "Globex",
            "country": "Germany",
        }
    ]


@pytest.mark.parametrize(
    "query",
    ["min_age", "limit", "offset"],
)
def test_get_users_with_negative_pagination_and_filters(test_client, query):
    response = test_client.get(f"/users?{query}=-1")
    assert response.status_code == 400
