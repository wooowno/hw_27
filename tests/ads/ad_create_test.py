import pytest


@pytest.mark.django_db
def test_create_ad(client, auth_token):
    expected_response = {
        "id": 1,
        "name": "test",
        "slug": "test",
        "author": None,
        "price": 100,
        "description": "test",
        "is_published": False,
        "image": None,
        "category": None,
    }

    data = {
        "name": "test",
        "slug": "test",
        "price": 100,
        "description": "test",
    }

    response = client.post(
        "/ad/create/",
        data,
        content_type="application/json",
        HTTP_AUTHORIZATION="Bearer" + auth_token
    )

    assert response.status_code == 201
    assert response.body == expected_response
